import streamlit as st
import pandas as pd
from PIL import Image
import folium
from folium import Marker
from streamlit_folium import st_folium, folium_static
from folium.plugins import Search
import requests



st.markdown("<h1 style='text-align: center;'>우리의 안전은 내가 지킨다!</h1>", unsafe_allow_html=True)
st.title(':superhero::female_superhero::male_superhero::male_superhero::female_superhero::superhero::superhero::female_superhero::male_superhero::male_superhero::female_superhero:')
st.divider()
st.video('https://www.youtube.com/watch?v=301Ticksx00', format="video/mp4", start_time=0)


st.header("학습목표 :book:")
st.subheader(":blue[[사회]] 위기 상황에 맞는 적절한 지리 정보를 활용하여 안전을 지키는 방법을 설명할 수 있다.")
st.subheader(":blue[[정보]] 사례를 중심으로 데이터 간의 관계를 파악하고, 데이터에 기반하여 의사결정을 할 수 있다.")
st.subheader(":blue[[수학]] 공학적 도구를 이용하여 지리 정보 데이터를 그래프로 나타내고, 그래프의 의미를 해석할 수 있다.")


st.divider()
st.header("지난 시간 복습")

st.subheader(":gray[지난 시간에 배웠던] :blue[위도]:gray[와] :blue[경도]:gray[를 떠올려 봅시다.]")

wmp = Image.open('saves/wmp.png')

st.image(wmp, caption='위도와 경도')
school_lat=37.472
school_lon=127.092
row1 = st.columns([1,1,1])
row1[0].write('지도를 보고 우리 학교의 **위도**와 **경도**를 예상해봅시다')
with st.form("form"):
    sch_lat = row1[1].text_input("우리 학교의 위도")
    sch_lon= row1[2].text_input("우리 학교의 경도")
    button=st.form_submit_button('과연 예상한 곳은?')
    
    if button:
        m1 = folium.Map(location=[sch_lat, sch_lon], zoom_start=20)
        Marker([sch_lat, sch_lon],popup='예상한 위도와 경도',icon=folium.Icon(color='blue',icon='star')).add_to(m1)
        folium_static(m1)
        st.write(f'실제 우리 학교의 위도는 {school_lat}이고 경도는 {school_lon}입니다')
        st.write('값이 조금만 달라져도 매우 멀어지는군요!')
    
st.header("우리 집의 위도와 경도 찾기:derelict_house_building:")


st.write('지도에서 우리 집의 위치를 클릭한 후, 팝업창의 확인을 누르고')
st.write('아래 [우리 집의 위도와 경도를 제출하기]를 눌러주세요')

m2 = folium.Map(control_scale=True)

m2.add_child(folium.LatLngPopup())

map = st_folium(m2, height=350, width=700)


if 'home_lon' not in st.session_state:
    st.session_state['home_lon'] = 0
    st.session_state['home_lat'] = 0


if map['last_clicked'] is not None:
    h_lat=map['last_clicked']['lat']
    h_lon=map['last_clicked']['lng']
    
    
    st.write(f'우리 집의 위도는 {h_lat}, 경도는 {h_lon}입니다')
    

    

b1=st.button("우리 집의 위도와 경도 제출하기")
if b1:

    st.session_state['home_lon'] = h_lon
    st.session_state['home_lat'] = h_lat
    st.write('다음 활동을 진행해봅시다.:grin:')


with st.form("form2"):
    st.subheader('지도에서 우리 집을 찾기 힘들다면 검색 후 아래에 입력해주세요 :red[(지도에서 찾았으면 입력 :x:)]')
    row2 = st.columns([1,1])
    h_lat1 = row2[0].text_input("우리 집의 위도")
    h_lon1 = row2[1].text_input("우리 집의 경도")
    b2=st.form_submit_button('우리 집의 위도와 경도 제출하기')
if b2:
    
    st.session_state['home_lon'] = h_lon1
    st.session_state['home_lat'] = h_lat1
    st.write('다음 활동을 진행해봅시다.:grin:')
if 'manual' not in st.session_state:
    st.session_state['manual']=pd.DataFrame({'Q':[], 'A':[]})
st.subheader("개인 활동 혹은 조별 활동이 끝나면 아래 버튼을 눌러")
st.subheader("파일을 다운받고 구글클래스에 제출해주세요")
filename=st.text_input("개인 활동이라면 **학번과 이름**, 조별 활동이라면 **조** **이름과** **반**을 입력해주세요")

st.download_button(
    label="활동 파일 다운로드 받기",
    data=st.session_state['manual'].to_csv(index=False).encode('cp949'),
    file_name=f'{filename}.csv',
    mime='csv',
)


