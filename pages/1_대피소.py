#10_schoolmap.py

import streamlit as st
import pandas as pd
from haversine import haversine
import folium
from folium import Marker
from streamlit_folium import st_folium, folium_static
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import urllib.request
import koreanize_matplotlib


home_lon=st.session_state['home_lon']
home_lat=st.session_state['home_lat']
 

st.title("1.대피소")

df = pd.read_csv("./saves/전국지진해일대피소표준데이터.csv")
df.dropna(subset = ['위도','경도'],inplace=True)

df['city'] = df['제공기관명'].apply(lambda x: x.split()[0])
with st.form("my_form"):
    header = st.columns([1])
    header[0].subheader('우리 동네 대피소 찾기')
    
    
    
    row2 = st.columns([1,1,1])
    home = row2[0].text('어떤 대피소를 볼까요?')
    type1= row2[1].multiselect("대피소유형",df["지진해일대피소유형구분"].unique())
    type2 = row2[2].multiselect("내진적용여부",df["내진적용여부"].unique())
    
    row3=st.columns([1,1,1])
    city=row3[1].multiselect("대피소 지역",df["city"].unique())
    button=st.form_submit_button('Update map')
df1=df.copy()
if button:
    
    
    if type1:    
        df1 = df1[df1["지진해일대피소유형구분"].isin(type1)]
    
    if type2:    
        df1 = df1[df1["내진적용여부"].isin(type2)]
        
    if city:
        df1=df1[df1["city"].isin(city)]
    
    
    df1 = df1.reset_index()
    
    def create_popup(home_lat, home_lon, data):
        distance = haversine((float(home_lat), float(home_lon)), (float(data['위도']), float(data['경도'])), unit='km')
        name=data['지진해일대피소명']
        type=data['지진해일대피소유형구분']
        mp=data['최대수용인원수']
        html = f'대피소 이름: {name} <br> 거리: {distance:.2f} km <br> 유형: {type} <br> 최대수용인원수:{mp:.0f}명'
        iframe = folium.IFrame(html,
                        width=300,
                        height=100)

        popup = folium.Popup(iframe,
                        max_width=300)
        
        return popup

    m1 = folium.Map(location=[home_lat, home_lon], zoom_start=20)
    Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m1)
    

    
    df1.apply(lambda row:Marker(location=[row["위도"],row["경도"]],icon=folium.Icon(color='green'),
                               popup=create_popup(home_lat, home_lon, row)).add_to(m1),axis=1)
    df1.apply(lambda row:folium.Circle(location=[row["위도"],row["경도"]],color='green',fill=True,fill_color='green',radius=row['최대수용인원수']/100).add_to(m1),axis=1)
    
    folium_static(m1)
if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = True
st.divider()    
st.subheader('어디로 대피할까?')
st.write('수용인원, 대피소 유형, 거리 등을 고려하여 어디로 대피를 해야할지 매뉴얼을 작성해봅시다')
sheltername=st.text_input("대피할 대피소 이름(클릭 후 뜨는 대피소 이름을 복사, 붙여넣기 해주세요)")
button2=st.button('대피소 제출',on_click=click_button())


if st.session_state.button:
    sh_d = df[df["지진해일대피소명"].isin([sheltername])]
    
    if len(sh_d)==0:
        st.write('대피소명을 다시 확인해주세요!')
    else:    
        
        st.write('대피하는 경로를 고려하여 거리를 구해봅시다')
        m2 = folium.Map(location=[home_lat, home_lon], zoom_start=20)
        Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m2)
        Marker([sh_d['위도'], sh_d['경도']],popup='대피소',icon=folium.Icon(color='red')).add_to(m2)
        folium.plugins.Draw(export=False).add_to(m2)
        folium_static(m2)
        with st.form("form2"):
            mydist=st.text_input("대피소까지의 거리(m)를 입력해주세요.(숫자만 입력)")
            mytime=st.text_input("빨리 걸을 때 여러분의 속력이 5km/h이라면 대피할 때 걸리는 시간은 몇 분인가요? (숫자만 입력)")
            mydist=float(mydist)
            mytime=float(mytime)
         
            button4=st.form_submit_button('제출하기')
            if button4:
              
              if int(mydist/500*6)<=mytime<=int(mydist/500*6)+1:
                st.write("거리와 속력으로 대피 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
              else:
                st.write("대피 시간을 다시 계산해봅시다! 단위를 주의해주세요")
        manual1=st.text_input("대피 시간, 계단, 대피 요령 등을 고려하여 대피 매뉴얼을 적어봅시다.")
        button6=st.button('매뉴얼 제출하기')
                
        
st.divider()
st.subheader('지역별로 대피소 유형은 어떨까?')
font_url ='https://github.com/yelin563/project2/blob/main/saves/NanumGothic.ttf'
urllib.request.urlretrieve(font_url, "NanumGothic.ttf")

plt.rcParams['font.family'] = 'NanumGothic'
city2=st.selectbox("대피소 지역",df["city"].unique(), placeholder="Choose an option")
button3=st.button('지역별 대피소 유형 보기')
if button3:
    city2_data = df[df["city"].isin([city2])]['지진해일대피소유형구분'].value_counts()
    fig, ax = plt.subplots()
    city2_data.plot.pie(fontsize=15, labels=city2_data.index, ax=ax)

    plt.title(f'{city2} 지진해일대피소유형구분', fontsize=20)

    st.pyplot(fig)
    
st.text_input("원 그래프를 통해 알게 된 사실을 공유해봅시다.")  

