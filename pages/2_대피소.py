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

import koreanize_matplotlib
from PIL import Image

home_lon=st.session_state['home_lon']
home_lat=st.session_state['home_lat']
def click_button(b):
    st.session_state[b] = True

st.title("1.대피소")

df = pd.read_csv("./saves/전국지진해일대피소표준데이터.csv")
df.dropna(subset = ['위도','경도'],inplace=True)

df['city'] = df['제공기관명'].apply(lambda x: x.split()[0])
if 'button21' not in st.session_state:
    st.session_state.button21 = False
if 'button22' not in st.session_state:
    st.session_state.button22 = False
if 'button23' not in st.session_state:
    st.session_state.button23 = False
if 'button24' not in st.session_state:
    st.session_state.button24 = False
if 'button25' not in st.session_state:
    st.session_state.button25 = False
with st.form("my_form"):
    header = st.columns([1])
    header[0].subheader('1) 우리 동네 대피소 찾기')
    row2 = st.columns([1,1,1])
    home = row2[0].text('어떤 대피소를 볼까요?')
    type1= row2[1].multiselect("대피소유형",df["지진해일대피소유형구분"].unique())
    type2 = row2[2].multiselect("내진적용여부",df["내진적용여부"].unique())
    
    row3=st.columns([1,1,1])
    city=row3[1].multiselect("대피소 지역",df["city"].unique())
    st.form_submit_button('Update map', on_click=click_button, args=("button21",))
    
    
df1=df.copy()
if st.session_state.button21:
    
    
    if type1:    
        df1 = df1[df1["지진해일대피소유형구분"].isin(type1)]
    
    if type2:    
        df1 = df1[df1["내진적용여부"].isin(type2)]
        
    if city:
        df1=df1[df1["city"].isin(city)]
    
    
    df1 = df1.reset_index()
    
    

    m1 = folium.Map(location=[home_lat, home_lon], zoom_start=20)
    Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m1)
    

    
    df1.apply(lambda row:Marker(location=[row["위도"],row["경도"]],icon=folium.Icon(color='green'),
                               popup=row['지진해일대피소명']).add_to(m1),axis=1)
    df1.apply(lambda row:folium.Circle(location=[row["위도"],row["경도"]],color='green',fill=True,fill_color='green',radius=row['최대수용인원수']/100).add_to(m1),axis=1)
    
    map=st_folium(m1,width=725,height=400)
    st.write("대피소 정보 확인하기")
    sheltername=map['last_object_clicked_popup']
    st.write(sheltername)
    sh_d = df[df["지진해일대피소명"].isin([sheltername])]
    
    st.write(sh_d)
    st.write('수용인원, 대피소 유형, 거리 등을 고려하여 대피할 대피소를 확정해봅시다')
    st.button("대피소 확정하기", on_click=click_button,args=('button22',))



     
st.divider()


    



if st.session_state.button22:
    
    
    st.subheader('2) 대피소까지의 거리를 측정하고 걸리는 시간 구해보기')
        
    st.write('대피하는 경로를 고려하여 거리를 구해봅시다')
    m2 = folium.Map(location=[home_lat, home_lon], zoom_start=20)
    Marker([home_lat, home_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m2)
    Marker([sh_d['위도'], sh_d['경도']],popup='대피소',icon=folium.Icon(color='red')).add_to(m2)
    folium.plugins.Draw(export=False).add_to(m2)
    folium_static(m2,width=725,height=400)
    with st.form("form2"):
        mydist=st.text_input("대피소까지의 거리(m)를 입력해주세요.(숫자만 입력)")
        mytime=st.text_input("빨리 걸을 때 여러분의 속력이 5km/h이라면 대피할 때 걸리는 시간은 몇 분인가요? (숫자만 입력)")
        button4=st.form_submit_button('제출하기', on_click=click_button,args=('button23',))
        

if st.session_state.button23:
    mydist=float(mydist)
    mytime=float(mytime)
    if int(mydist/500*6)<=mytime<=int(mydist/500*6)+1:
        st.write("거리와 속력으로 대피 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
        st.button('다음 활동 진행하기', on_click=click_button, args=("button24",))
    else:
        st.write("대피 시간을 다시 계산해봅시다! 단위를 주의해주세요")
        
if 'manual' not in st.session_state:
    st.session_state['manual']=pd.DataFrame({'Q':[], 'A':[]})
def addresponse(q,a):
    new_row = pd.Series({'Q': q, 'A': a})
    st.session_state['manual'] = st.session_state['manual'].append(new_row, ignore_index=True)
   
if st.session_state.button24:
    st.divider()
    st.subheader("3) 대피소까지의 매뉴얼 작성해보기")
    manual1=st.text_input("상황을 구체적으로 설정하고 대피 시간, 계단, 대피 요령 등을 고려하여 대피 매뉴얼을 적어봅시다.")
    row1 = st.columns([1,1])
    row1[0].button('매뉴얼 제출하기', on_click=addresponse , args=('대피소매뉴얼',manual1))
    


        
    st.divider()
    
    st.subheader('4)지역별로 대피소 유형은 어떨까?')


    plt.rcParams['font.family'] = 'NanumGothic'
    city2=st.selectbox("대피소 지역",df["city"].unique(), placeholder="Choose an option")
    button3=st.button('지역별 대피소 유형 보기')
    if button3:
        city2_data = df[df["city"].isin([city2])]['지진해일대피소유형구분'].value_counts()
        
        st.bar_chart(data=city2_data)
        
    answer=st.text_input("막대 그래프를 통해 알게 된 사실을 공유해봅시다.")
    st.button('제출하기', on_click=addresponse , args=('대피소 막대 그래프',answer))
  
