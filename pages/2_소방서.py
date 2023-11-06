#10_schoolmap.py

import streamlit as st
import pandas as pd

import folium
from folium import Marker
from streamlit_folium import st_folium, folium_static
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request
import requests
from branca.colormap import linear

home_lon=st.session_state['home_lon']
home_lat=st.session_state['home_lat']


geo_data = requests.get(
    "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo.json").json()

df119 = pd.read_csv("./saves/119안전센터.csv")
dict119 = df119.set_index("구")["119안전센터(개소)"]
df119loc=pd.read_csv("./saves/119안전센터위치.csv")
df1=pd.read_csv("./saves/119구급활동.csv")
dict1 = df1.set_index("구")["구급 출동건수"]
df2=pd.read_csv("./saves/119구조활동.csv")
dict2 = df2.set_index("구")["구조 출동건수"]
st.title("2.소방서")

st.divider()
st.subheader('1) 가장 가까운 119안전센터는 어디일까?')
st.write('구급대가 가까운 119안전센터에서 출발하면 어떤 경로로 올지 예상해봅시다')


m = folium.Map(location=[home_lat, home_lon], zoom_start=20)
Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m)

df119loc.apply(lambda row:Marker(location=[row["위도"],row["경도"]],icon=folium.Icon(color='green'),
                            popup=row['센터명']).add_to(m),axis=1)
folium.plugins.Draw(export=False).add_to(m)
folium_static(m)

with st.form("form"):
            mydist=st.text_input("구급대의 예상 이동거리를 입력해주세요")
            manual1=st.text_input("예상 이동 시간은 몇 분 일까요?")
            button1=st.form_submit_button('제출하기')
if button1:
    st.write('구급대의 현장도착까지의 평균 이동시간은 10분이라고 하네요. 예상시간과 평균시간을 비교하고 공유해봅시다')
            

st.divider()

st.subheader('2) 구별로 119안전센터가 얼마나 많을까?')


m1 = folium.Map([37.55, 127], zoom_start=11)
colormap = linear.YlGn_09.scale(
    df119['119안전센터(개소)'].min(), df119['119안전센터(개소)'].max()
)


folium.GeoJson(
    geo_data,
    name="119안전센터 수",
    style_function=lambda feature: {
        "fillColor": colormap(dict119[feature["properties"]["name"]]),
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.7,
    },tooltip=folium.GeoJsonTooltip(
        fields=["name"],  
         
        localize=True,
        sticky=False,
        labels=True,
        max_width=800,
    )
).add_to(m1)
colormap.caption = "119안전센터 수"
colormap.add_to(m1)


Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m1)
fg = folium.FeatureGroup(name="119안전센터위치", show=False).add_to(m1)
df119loc.apply(lambda row:Marker(location=[row["위도"],row["경도"]],icon=folium.Icon(color='green'),
                               popup=row['센터명']).add_to(fg),axis=1)

folium.LayerControl().add_to(m1)
folium_static(m1)

st.subheader('구별로 구급,구조 출동건수가 얼마나 많을까?')
m2 = folium.Map([37.55, 127], zoom_start=11)
colormap2 = linear.YlOrRd_09.scale(df1['구급 출동건수'].min(), df1['구급 출동건수'].max())
colormap3 = linear.PuBu_09.scale(df2['구조 출동건수'].min(), df2['구조 출동건수'].max())

folium.GeoJson(
    geo_data,
    name="구급 출동건수",
    style_function=lambda feature: {
        "fillColor": colormap2(dict1[feature["properties"]["name"]]),
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.7,
    },tooltip=folium.GeoJsonTooltip(
        fields=["name"],  
         
        localize=True,
        sticky=False,
        labels=True,
        max_width=800,
    )).add_to(m2)
folium.GeoJson(
    geo_data,
    name="구조 출동건수",
    style_function=lambda feature: {
        "fillColor": colormap3(dict2[feature["properties"]["name"]]),
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.7,
    },tooltip=folium.GeoJsonTooltip(
        fields=["name"],  
         
        localize=True,
        sticky=False,
        labels=True,
        max_width=800,
    )).add_to(m2)
Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m2)
colormap2.caption = "구급 출동건수"
colormap2.add_to(m2)
colormap3.caption = "구조 출동건수"
colormap3.add_to(m2)
folium.LayerControl().add_to(m2)
folium_static(m2)
st.divider()
st.subheader('3) 119안전센터의 갯수와 출동건수')

newdf= pd.merge(df119, df1,on='구')
newdf= pd.merge(newdf, df2,on='구')
newdf['센터당 구급 출동건수']=newdf['구급 출동건수']/newdf['119안전센터(개소)']
newdf['센터당 구조 출동건수']=newdf['구조 출동건수']/newdf['119안전센터(개소)']
newdict1= newdf.set_index("구")["센터당 구급 출동건수"]
newdict2= newdf.set_index("구")["센터당 구조 출동건수"]
with st.form("form2"):
            x=st.selectbox("x축",['구급 출동건수','구조 출동건수','119안전센터(개소)'], placeholder="Choose an option")
            y=st.selectbox("y축",['구급 출동건수','구조 출동건수','119안전센터(개소)'], placeholder="Choose an option")
            button2=st.form_submit_button('제출하기')
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = True

if button2:
    
    st.scatter_chart(
        newdf,
        x=x,
        y=y
    )
  st.write("구 별로 안전센터의 개수와 출동 건수가 다른 이유는 무엇일까요?) 
  button4=st.button('119안전센터 설치기준 보기',on_click=click_button())
  



colormap4 = linear.YlOrRd_09.scale(newdf['센터당 구급 출동건수'].min(), newdf['센터당 구급 출동건수'].max())
colormap5 = linear.PuBu_09.scale(newdf['센터당 구조 출동건수'].min(), newdf['센터당 구조 출동건수'].max())

if st.session_state.button:
    img = Image.open(r'/saves/안전센터설치기준.png')

    st.image(img, caption='119안전센터 설치기준')
    st.write('인구가 많은 지역에 119안전센터를 많이 짓고 인구가 많은 지역에 출동건수가 많기 때문이었네요!')
    
    st.write('구의 인구에 맞춰 119안전센터를 지었으니 119안전센터별 출동건수는 모두 비슷할까요?')
    st.write('119안전센터가 가장 바쁜 구와 가장 여유로운 구는 어디일까요?')
    st.divider()
    st.subheader("4) 119안전센터 당 출동건수")
    with st.form("form3"):
        st.write("각 구 별로 어떤 계산을 해봐야 할까요?")
        row1 = st.columns([1,1,1])
       
        a1=row1[0].selectbox("",['출동건수','119 안전센터 갯수','위도','경도'], placeholder="Choose an option",key='a1')
        a2=row1[1].selectbox("",["더하기","빼기","곱하기","나누기"], placeholder="Choose an option",key='a2')
        a3=row1[2].selectbox("",['출동건수','119 안전센터 갯수','위도','경도'], placeholder="Choose an option",key='a3')
        button5=st.form_submit_button('제출하기') 
    if button5:
        if a1=='출동건수' and a2=='나누기' and a3=='119 안전센터 갯수':
            st.write('맞아요! 그러면 구 별 119 안전센터 당 출동건수를 살펴봅시다')
            
            m3 = folium.Map([37.55, 127], zoom_start=11)
            
            folium.GeoJson(
                geo_data,
                name="센터당 구급 출동건수",
                style_function=lambda feature: {
                    "fillColor": colormap4(newdict1[feature["properties"]["name"]]),
                    "color": "black",
                    "weight": 1,
                    "dashArray": "5, 5",
                    "fillOpacity": 0.7,
                },tooltip=folium.GeoJsonTooltip(
                    fields=["name"],  
                    
                    localize=True,
                    sticky=False,
                    labels=True,
                    max_width=800,
                )
            ).add_to(m3)
            colormap4.caption = "119안전센터당 구급 출동건수"
            colormap4.add_to(m3)
            
            folium.GeoJson(
                geo_data,
                name="센터당 구조 출동건수",
                style_function=lambda feature: {
                    "fillColor": colormap5(newdict2[feature["properties"]["name"]]),
                    "color": "black",
                    "weight": 1,
                    "dashArray": "5, 5",
                    "fillOpacity": 0.7,
                },tooltip=folium.GeoJsonTooltip(
                    fields=["name"],  
                    
                    localize=True,
                    sticky=False,
                    labels=True,
                    max_width=800,
                )
            ).add_to(m3)
            colormap5.caption = "119안전센터당 구조 출동건수"
            colormap5.add_to(m3)


            Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m3)
            

            folium.LayerControl().add_to(m3)
            folium_static(m3)
            
            st.write("서울에 새로운 119안전센터를 지으면 좋을 곳을 공유해봅시다")
        else:
            st.write("다시 생각해봅시다")
                
