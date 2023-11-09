#10_schoolmap.py

import streamlit as st
import pandas as pd
from PIL import Image
import folium
from folium import Marker
from streamlit_folium import st_folium, folium_static
import matplotlib
import matplotlib.pyplot as plt

import requests
from branca.colormap import linear


school_lat=37.46
school_lon=126.956
df1=pd.read_csv("./saves/서울시 응급실 위치 정보.csv")
df2= pd.read_csv("./saves/전국지진해일대피소표준데이터.csv")
df2.dropna(subset = ['위도','경도'],inplace=True)
df2['city'] = df2['제공기관명'].apply(lambda x: x.split()[0])
df2=df2[df2["city"].isin(['서울특별시'])]
df3=pd.read_csv("./saves/119안전센터위치.csv")
def addresponse(q,a):
    new_row = pd.Series({'Q': q, 'A': a})
    st.session_state['manual'] = st.session_state['manual'].append(new_row, ignore_index=True)
geo_data = requests.get(
    "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo.json").json()
x=st.selectbox("조별로 진행할 활동 주제를 고르세요",['선택없음','응급실과 119안전센터','대피소'], placeholder="Choose an option")

st.divider()

def click_button(b):
    st.session_state[b] = True
for i in range(1,10):
    if f'button4{i}' not in st.session_state:
        st.session_state[f'button4{i}'] = False

if x=='응급실과 119안전센터':
    st.title("학교에서 다쳤을 때 매뉴얼 작성하기")
    st.subheader("1) 학교에서 가장 가까운 119안전센터는?")
    s1=st.text_area("학교에서 친구 혹은 자신이 다쳤을 때의 상황을 구체적으로 설정해봅시다.(시간,이유,장소,주변상황 등)")
    st.write('119에 신고를 했을 때 구급대가 어떤 경로로 몇 분 후에 올지 예상해봅시다')
    m = folium.Map(location=[school_lat, school_lon], zoom_start=20)
    Marker([school_lat, school_lon],popup='학교',icon=folium.Icon(color='blue',icon='star')).add_to(m)

    df3.apply(lambda row:Marker(location=[row["위도"],row["경도"]],icon=folium.Icon(color='green'),
                                popup=row['센터명']).add_to(m),axis=1)
    folium.plugins.Draw(export=False).add_to(m)

    folium_static(m)
    st.subheader("2) 구급차의 출동 시간 확인하기")
    with st.form("form"):
            mydist=st.text_input("구급대가 해당 119안전센터에서 출발했을때 학교까지의 구급대의 예상 이동거리를 입력해주세요")
            mytime=st.text_input("구급대의 평균 속력이 20km/h이라면 출동에 걸리는 시간은 몇 분인가요? (숫자만 입력)")
            
            st.form_submit_button('제출하기', on_click=click_button, args=("button41",))
    if st.session_state.button41:
        mydist=float(mydist)
        mytime=float(mytime)
        if int(mydist/2000*6)<=mytime<=int(mydist/2000*6)+1:
            st.write("거리와 속력으로 구급대의 출동 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
            
            st.button('다음 활동 진행하기', on_click=click_button, args=("button42",))
        else:
            st.write("시간을 다시 계산해봅시다! 단위를 주의해주세요")
    if st.session_state.button42:
        st.subheader("3) 응급 처치하기")
        manual1=st.text_area("구급대가 도착할 때까지의 시간동안 어떤 처치를 할 지 작성해봅시다. 제출 후 다음 활동 진행하기 버튼을 눌러주세요.")
        st.button('제출하기', on_click=addresponse , args=('조)응급실과 안전센터',s1+'\n'+manual1))
        st.button('다음 활동 진행하기', on_click=click_button, args=("button43",),key='b43')
        
    if st.session_state.button43:
        st.subheader("4) 학교 근처 응급실은?")
        st.write('이제 학교에서 근처 응급실로 갈 때의 경로와 시간을 예상해봅시다.')
        st.write('응급실 정보, 거리, 영업시간, 점심시간 등을 확인하고 응급실을 확정해주세요.')

        m1 = folium.Map(location=[school_lat, school_lon], zoom_start=20)
        Marker([school_lat, school_lon], popup='학교', icon=folium.Icon(color='blue', icon='star')).add_to(m1)

        df1.apply(lambda row:Marker(location=[row["병원위도"], row["병원경도"]], icon=folium.Icon(color='green'), popup=row['기관명']).add_to(m1), axis=1)
        folium.plugins.Draw(export=False).add_to(m1)
        map=st_folium(m1,width=725,height=400)
        st.write("응급실 정보 확인하기")
        
        hosname=map['last_object_clicked_popup']
        st.write(hosname)
        ho_d = df1[df1["기관명"].isin([hosname])]
        st.write(ho_d)
        st.button("응급실 확정하기", on_click=click_button, args=("button44",))

    if st.session_state.button44:
        st.subheader("4) 응급실까지의 경로와 시간 확인하기")
        with st.form("form2"):
        
            mydist1=st.text_input("응급실까지의 거리(m)를 입력해주세요.(숫자만 입력)")
            mytime1=st.text_input("구급대의 평균 속력이 20km/h이라면 응급실까지 걸리는 시간은 몇 분인가요? (숫자만 입력)")
            
            st.form_submit_button('제출하기', on_click=click_button, args=("button45",))
    if st.session_state.button45:
        mydist1=float(mydist1)
        mytime1=float(mytime1)
        if int(mydist1/2000*6)<=mytime1<=int(mydist1/2000*6)+1:
            st.write("거리와 속력으로 응급실까지 가는 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
            
            st.button('다음 활동 진행하기', on_click=click_button, args=("button46",),key='b46')
        else:
            st.write("시간을 다시 계산해봅시다! 단위를 주의해주세요")
    if st.session_state.button46:
        st.subheader("5) 우리학교 안전수칙")
        st.write("우리의 안전은 우리가 지킨다! 우리 학교 근처 응급실, 119안전센터를 살펴보며 미리 위급 상황을 대비해봤어요.")
        st.write("위급 상황일 때 당황하지 않을 수 있겠죠? 하지만 다치치 않는 것이 가장 최선!")
        an3=st.text_area("우리 학교에서 지켜야 할 안전 수칙을 3가지 적어봅시다")
        button6=st.button('제출하기', on_click=addresponse , args=('조)학교 안전수칙',an3),key='b6')
        if button6:
            st.write("조별 활동 끝! 첫 페이지로 돌아가 파일을 다운 받고 제출해주세요")

st.divider()
img1 = Image.open('saves/행동요령1.jpg')
img2 = Image.open('saves/행동요령2.jpg')

if x=='대피소':
    
    
    st.title("학교에서 대피소까지의 대피 매뉴얼 작성하기")
    st.subheader("1) 학교에서 가장 가까운 대피소는?")
    s2=st.text_area("학교에서 대피해야 하는 상황을 구체적으로 설정해봅시다.(시간,이유,장소,주변상황 등)")
    st.write('대피소로 어떤 경로로 갈지 생각해봅시다')
    

    

    m2 = folium.Map(location=[school_lat, school_lon], zoom_start=20)
    Marker([school_lat, school_lon],popup='학교',icon=folium.Icon(color='blue',icon='star')).add_to(m2)
    

    
    df2.apply(lambda row:Marker(location=[row["위도"],row["경도"]],popup=row['지진해일대피소명'],icon=folium.Icon(color='green')).add_to(m2),axis=1)
    df2.apply(lambda row:folium.Circle(location=[row["위도"],row["경도"]],color='green',fill=True,fill_color='green',radius=row['최대수용인원수']/100).add_to(m2),axis=1)
    map2=st_folium(m2,width=725,height=400)
    st.subheader("2) 대피소 정보 확인하기")
    sheltername=map2['last_object_clicked_popup']
    st.write(sheltername)
    sh_d = df2[df2["지진해일대피소명"].isin([sheltername])]
    
    st.write(sh_d)
    st.write('수용인원, 대피소 유형, 거리 등을 고려하여 대피할 대피소를 확정해봅시다')
    st.button("대피소 확정하기", on_click=click_button,args=('button47',))

    if st.session_state.button47:
        st.subheader("3) 대피 경로 확인하기")
        st.write('대피하는 경로를 고려하여 거리를 구해봅시다')
        m3 = folium.Map(location=[school_lat, school_lon], zoom_start=20)
        Marker([school_lat, school_lon],popup='우리집',icon=folium.Icon(color='blue',icon='star')).add_to(m3)
        Marker([sh_d['위도'], sh_d['경도']],popup='대피소',icon=folium.Icon(color='red')).add_to(m3)
        folium.plugins.Draw(export=False).add_to(m3)
        folium_static(m3,width=725,height=400)
        with st.form("form2"):
            mydist2=st.text_input("대피소까지의 거리(m)를 입력해주세요.(숫자만 입력)")
            mytime2=st.text_input("빨리 걸을 때 여러분의 속력이 5km/h이라면 대피할 때 걸리는 시간은 몇 분인가요? (숫자만 입력)")
            button4=st.form_submit_button('제출하기', on_click=click_button,args=('button48',))
        
    if st.session_state.button48:
        mydist2=float(mydist2)
        mytime2=float(mytime2)
        if int(mydist2/500*6)<=mytime2<=int(mydist2/500*6)+1:
            st.write("거리와 속력으로 대피 시간을 잘 계산했네요! 다음 활동을 진행해주세요.")
            st.button('다음 활동 진행하기', on_click=click_button, args=("button49",))
        else:
            st.write("대피 시간을 다시 계산해봅시다! 단위를 주의해주세요")
    if st.session_state.button49:
        st.subheader("4) 대피 매뉴얼 작성 하기")  
        manual2=st.text_area("대피 시간, 계단, 대피 요령 등을 고려하여 대피 매뉴얼을 적어봅시다.링크와 사진을 참고하세요!")
        st.link_button('지진, 해일 행동요령 링크','https://www.weather.go.kr/w/eqk-vol/baro/evacuation.do')
        button5=st.button('비상시 행동요령 보기')
        if button5:
            st.image(img1, caption='비상시 행동요령')
            st.image(img2, caption='비상시 행동요령')
        button6=st.button('매뉴얼 제출하기', on_click=addresponse , args=('조)대피소매뉴얼',s2+'\n'+manual2))
        if button6:
            st.write("우리의 안전은 우리가 지킨다! 우리 학교 근처 대피소를 살펴보며 미리 위급 상황을 대비해봤어요.")
            st.write("위급 상황일 때 당황하지 않을 수 있겠죠?")
            st.write("조별 활동이 끝났으니 첫 페이지로 돌아가 파일을 다운 받고 제출해주세요")