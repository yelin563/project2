#10_schoolmap.py

import streamlit as st
import pandas as pd

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
df=pd.read_csv("./saves/서울시 응급실 위치 정보.csv")

geo_data = requests.get(
    "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo.json").json()
st.title("1.응급실:ambulance:")

st.divider()
st.subheader("우리 집에서가장 가까운 응급실은 어디일까:question:")




def click_button(b):
    st.session_state[b] = True

m = folium.Map(location=[home_lat, home_lon], zoom_start=20)
Marker([home_lat, home_lon], popup='우리집', icon=folium.Icon(color='blue', icon='star')).add_to(m)

df.apply(lambda row:Marker(location=[row["병원위도"], row["병원경도"]], icon=folium.Icon(color='green'), popup=row['기관명']).add_to(m), axis=1)
folium.plugins.Draw(export=False).add_to(m)
map=st_folium(m,width=725,height=400)
if 'button11' not in st.session_state:
    st.session_state.button11 = False
if 'button12' not in st.session_state:
    st.session_state.button12 = False
                    
if 'button13' not in st.session_state:
    st.session_state.button13 = False
st.subheader("응급실을 클릭하여 응급실 정보를 확인해보세요.")
hosname=map['last_object_clicked_popup']
st.write(hosname)
ho_d = df[df["기관명"].isin([hosname])]
st.write(ho_d)
st.write('진료 요일과 진료 시간 등을 고려하여 응급실을 선택해보세요.')
st.button("응급실 확정하기", on_click=click_button, args=("button11",))



if st.session_state.button11:
    with st.form("form2"):
        st.subheader("2) 거리를 측정하고 걸리는 시간을 구해보자:hourglass_flowing_sand:")
        mydist=st.text_input("응급실까지의 거리(m)를 입력해주세요.",placeholder="단위(m)를 제외하고 숫자만 입력해주세요.")
        mytime=st.text_input("구급대의 평균 속력이 20km/h이라면 응급실까지 걸리는 시간은 몇 분일까요?",placeholder="걸리는 시간은 자연수로 입력해주세요. 약간의 오차는 인정됩니다.")
        
        st.form_submit_button('제출하기', on_click=click_button, args=("button12",))
    

            


st.divider()         
if st.session_state.button12:
    mydist=float(mydist)
    mytime=float(mytime)
    if int(mydist/2000*6)<=mytime<=int(mydist/2000*6)+1:
        st.write("거리와 속력으로 응급실까지 가는 시간을 잘 계산했네요!	:+1: 다음 활동을 진행해주세요.")
        
        st.button('다음 활동 진행하기', on_click=click_button, args=("button13",))
    else:
        st.write("시간을 다시 계산해봅시다!:disappointed_relieved: 단위를 주의해주세요")
st.divider()

def addresponse(q,a):
    new_row = pd.Series({'Q': q, 'A': a})
    st.session_state['manual'] = st.session_state['manual'].append(new_row, ignore_index=True)
   
if st.session_state.button13:
    st.subheader("응급실까지의 매뉴얼 작성해보자:writing_hand:")
    manual1=st.text_input("응급실에 가야할 상황을 시간, 이유 등 구체적으로 설정하고 응급실 까지 가는 시간, 경로 등을 고려하여 매뉴얼을 적어봅시다.", key='manual1')
    
    st.write( ' :blue[예) 학교 수업 시간 중 다리가 다쳐서 응급실에 가야한다. 응급실에 갈 때...]')
    st.button('매뉴얼 제출하기', on_click=addresponse , args=('응급실매뉴얼',manual1))


st.divider()