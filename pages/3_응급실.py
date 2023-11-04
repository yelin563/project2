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
df=pd.read_csv("./saves/서울시 응급실 위치 정보.csv")

geo_data = requests.get(
    "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo.json").json()
st.title("3.응급실")
st.divider()
st.subheader("1) 가장 가까운 응급실은?")
st.write('응급실로 어떤 경로로 갈지 생각해봅시다')


m = folium.Map(location=[home_lat, home_lon], zoom_start=20)
Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m)

df.apply(lambda row:Marker(location=[row["병원위도"],row["병원경도"]],icon=folium.Icon(color='green'),
                            popup=row['기관명']).add_to(m),axis=1)
folium.plugins.Draw(export=False).add_to(m)
folium_static(m)
st.write("응급실 정보 확인하기")
hosname=st.text_input("검색할 응급실 이름(정확히 입력해주세요)")
button1=st.button('응급실 이름 제출하기')
if button1:
    ho_d = df[df["기관명"].isin([hosname])]
    
    if len(ho_d)==0:
        st.write('대피소명을 다시 확인해주세요!')
    else:    
        
        st.write(ho_d)
    
with st.form("form"):
            mydist=st.text_input("응급실까지 예상 이동거리를 입력해주세요")
            manual1=st.text_input("구급대를 이용했을 때 예상 이동 시간은 몇 분 인가요?")
            button1=st.form_submit_button('제출하기')
if button1:
    st.write('구급대의 현장에서 응급실까지의 평균 이동시간은 13분이라고 하네요. 예상시간과 평균시간을 비교하고 공유해봅시다')

st.divider()
