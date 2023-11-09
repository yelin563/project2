#10_schoolmap.py

import streamlit as st
import pandas as pd
from PIL import Image
import folium
from folium import Marker
from streamlit_folium import st_folium, folium_static
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

import requests
from branca.colormap import linear

home_lon=st.session_state['home_lon']
home_lat=st.session_state['home_lat']
def click_button(b):
    st.session_state[b] = True
if 'button31' not in st.session_state:
    st.session_state.button31 = False
if 'button32' not in st.session_state:
    st.session_state.button32 = False
                    
if 'button33' not in st.session_state:
    st.session_state.button33 = False
if 'button34' not in st.session_state:
    st.session_state.button34 = False
if 'button35' not in st.session_state:
    st.session_state.button35 = False
if 'button36' not in st.session_state:
    st.session_state.button36 = False
if 'button37' not in st.session_state:
    st.session_state.button37 = False
def addresponse(q,a):
    new_row = pd.Series({'Q': q, 'A': a})
    st.session_state['manual'] = st.session_state['manual'].append(new_row, ignore_index=True)
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
            mydist=st.text_input("구급대가 해당 119안전센터에서 출발했을때 집까지의 구급대의 예상 이동거리를 입력해주세요")
            mytime=st.text_input("구급대의 평균 속력이 20km/h이라면 출동에 걸리는 시간은 몇 분인가요? (숫자만 입력)")
            
            st.form_submit_button('제출하기', on_click=click_button, args=("button31",))
if st.session_state.button31:
    mydist=float(mydist)
    mytime=float(mytime)
    if int(mydist/2000*6)<=mytime<=int(mydist/2000*6)+1:
        st.write("거리와 속력으로 구급대의 출동 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
        
        st.button('다음 활동 진행하기', on_click=click_button, args=("button32",))
    else:
        st.write("시간을 다시 계산해봅시다! 단위를 주의해주세요")

    
            
if st.session_state.button32:
    st.divider()

    st.subheader('2) 구별 119안전센터 수의 출동건수')
    st.write("구별로 119안전센터가 얼마나 많을까?")


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

    st.write('구별로 구급,구조 출동건수가 얼마나 많을까?')
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
    with st.form("form1"):
        an1=st.selectbox("Q1-1)가장 구조 출동건수가 많은 구는 어디인가요?",df1['구'].unique(), placeholder="Choose an option")
        an2=st.selectbox("Q1-2)그 구의 119안전센터의 갯수는 몇개인가요?",[i for i in range(2,7)], placeholder="Choose an option")
        an3=st.selectbox("Q2-1)가장 구급 출동건수가 적은 구는 어디인가요?",df1['구'].unique(), placeholder="Choose an option")
        an4=st.selectbox("Q2-2)그 구의 119안전센터의 갯수는 몇개인가요?",[i for i in range(2,7)], placeholder="Choose an option")
        st.form_submit_button('확인하기', on_click=click_button, args=("button33",))
if st.session_state.button33:
    if an1=='강남구' and an2==6:
        if an3=='금천구' and an4==2:
            st.write("지도를 잘 해석했네요! 다음 활동으로 진행해주세요")
            st.button("다음 활동 진행하기", on_click=click_button, args=("button34",),key='b1')
        else:
            st.write("Q2를 다시 확인해주세요!")
    else:
        if an3=='금천구' and an4==2:
            st.write("Q1를 다시 확인해주세요!")
        else:
            st.write("지도를 다시 해석해봅시다. 지도 왼쪽 위에 있는 선의 색깔을 잘 봐주세요.")
newdf= pd.merge(df119, df1,on='구')
newdf= pd.merge(newdf, df2,on='구')
newdf['센터당 구급 출동건수']=newdf['구급 출동건수']/newdf['119안전센터(개소)']
newdf['센터당 구조 출동건수']=newdf['구조 출동건수']/newdf['119안전센터(개소)']
if st.session_state.button34:  
    st.divider()
    st.subheader('3) 119안전센터의 갯수와 출동건수')

    
    
    newdict1= newdf.set_index("구")["센터당 구급 출동건수"]
    newdict2= newdf.set_index("구")["센터당 구조 출동건수"]
    with st.form("form2"):
        st.write("한 눈에 구별 119안전센터와 출동건수를 보기 위해 좌표평면에 나타내볼까요?")
        st.write("119안전센터의 갯수를 x좌표로 표현하고, y좌표를 출동건수로 표현해봅시다")
        
        y=st.selectbox("y좌표",['구급 출동건수','구조 출동건수'], placeholder="Choose an option")
        button2=st.form_submit_button('제출하기', on_click=click_button, args=("button35",))


if st.session_state.button35:
    
    st.scatter_chart(
        newdf,
        x='119안전센터(개소)',
        y=y
    )
    st.write("구 별로 안전센터의 개수와 출동 건수가 다른 이유는 무엇일까요?") 
    st.button('119안전센터 설치기준 보기', on_click=click_button, args=("button36",))
        



colormap4 = linear.YlOrRd_09.scale(newdf['센터당 구급 출동건수'].min(), newdf['센터당 구급 출동건수'].max())
colormap5 = linear.PuBu_09.scale(newdf['센터당 구조 출동건수'].min(), newdf['센터당 구조 출동건수'].max())
img = Image.open('saves/img119.png')
if st.session_state.button36:  
       
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
        button5=st.form_submit_button('제출하기', on_click=click_button, args=("button37",)) 
if st.session_state.button37:
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
        ans1=st.text_input("금천구는 출동건수가 적은 구였지만 119 안전센터 당 출동건수가 높은 이유는 무엇일까요?")
        ans2=st.text_input("서울에 새로운 119안전센터를 지으면 좋은 곳을 적고 이유를 적어주세요('숭실대근처'처럼 구체적으로 표현해주세요)")
        st.button('제출하기', on_click=addresponse , args=('119 안전센터 당 출동건수',ans1+'\n'+ans2))   
    else:
        st.write("다시 생각해봅시다")