# sha 2024_05_06 국토교통부 데이터 수집 앱
# 행정안전부 주민등록,인감,행정사 행정동, 법정동 변경내역 조회
# https://www.mois.go.kr/frt/bbs/type001/commonSelectBoardList.do?bbsId=BBSMSTR_000000000052
# https://github.com/WooilJeong/PublicDataReader/blob/main/assets/docs/portal/BuildingLedger.md#%EA%B1%B4%EC%B6%95%EB%AC%BC%EB%8C%80%EC%9E%A5-%EC%B4%9D%EA%B4%84%ED%91%9C%EC%A0%9C%EB%B6%80-%EC%A1%B0%ED%9A%8C-%EC%84%9C%EB%B9%84%EC%8A%A4

import glob 
import os
import sys, subprocess
from subprocess import Popen, PIPE
import numpy as np
import pandas as pd

import streamlit as st
import sklearn
import seaborn as sns
# sns.set(font="D2Coding") 
# sns.set(font="Malgun Gothic") 
# from IPython.display import set_matplotlib_formats
# set_matplotlib_formats("retina")
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go 
# import chart_studio.plotly as py
# import cufflinks as cf
# # get_ipython().run_line_magic('matplotlib', 'inline')


# # Make Plotly work in your Jupyter Notebook
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
# init_notebook_mode(connected=True)
# # Use Plotly locally
# cf.go_offline()


# 사이킷런 라이브러리 불러오기 _ 통계, 학습 테스트세트 분리, 선형회귀등
from scipy import stats
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error 
from sklearn.metrics import r2_score 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import mean_squared_log_error
from PublicDataReader import BuildingLedger


# # hide the hamburger menu? hidden or visible
hide_menu_style = """
        <style>
        #MainMenu {visibility: visible;}
        footer {visibility: visible;}
        footer:after {content:'Copyright 2024. EAN_RU_BOMI. All rights reserved.';
        display:block;
        opsition:relatiive;
        color:orange; #tomato 
        padding:5px;
        top:100px;}

        </style>
        """

st.set_page_config(layout="wide", page_title="EAN_RU_BOMI_mois")
st.markdown(hide_menu_style, unsafe_allow_html=True) # hide the hamburger menu?









# 만료예정일 2024-10-12 만료 이후 재신청필요
# https://www.data.go.kr/iim/api/selectAcountList.do
# b7U179viBFuoc0q%2BDcekgsaFJsbHBZnIrgbl2ORvXCAB0Id0Sq954E%2Fju4FHtlWHU1AM9f9859c28%2FYGKKNPjQ%3D%3D
# b7U179viBFuoc0q+DcekgsaFJsbHBZnIrgbl2ORvXCAB0Id0Sq954E/ju4FHtlWHU1AM9f9859c28/YGKKNPjQ==

# 활용신청 상세기능정보
# https://www.data.go.kr/iim/api/selectAPIAcountView.do

service_key_1 = "b7U179viBFuoc0q%2BDcekgsaFJsbHBZnIrgbl2ORvXCAB0Id0Sq954E%2Fju4FHtlWHU1AM9f9859c28%2FYGKKNPjQ%3D%3D"
service_key_2 = "b7U179viBFuoc0q+DcekgsaFJsbHBZnIrgbl2ORvXCAB0Id0Sq954E/ju4FHtlWHU1AM9f9859c28/YGKKNPjQ=="
api = BuildingLedger(service_key_1)

# 기본개요, 교체표제부, 표제부, 바닥별개요 전유공용면적, 오수정화시설, 주택가격, 전유부, 지구 지역

import streamlit as st

# Assuming 'api' is your API handler object

df_legal_B = pd.read_csv('legal_info_b.csv')

st.caption('--------', unsafe_allow_html=False)
st.subheader('■ 건축물 대장 "총괄표제부"의 정보만 필요할 경우 아래 웹사이트에서 편하게 검색 가능합니다')
st.markdown('https://www.hub.go.kr/portal/gis/bld/idx-bld-polygon-list.do')
st.subheader('■ 층별개요 및 PK 번호 등 기타 표제부 외 정보 필요시 아래 주소검색과 서비스 선택')

st.caption('--------', unsafe_allow_html=False)
st.subheader('■ 주소검색')
st.markdown('1. 구, 군 단위일때, 시는 입력 하지 않음 ex)강남구/대치동 , 양평군/옥천면')
st.markdown('1-1. 특별시, 광역시, 자치시가 아닌 시에서 구 단위 구분 되어있다면 시 입력 ex)수원시 장안구/파장동 , 부천시 원미구/춘의동')
sigungu_input = st.text_input("시군구", "강남구")
bdong_input = st.text_input("법정동", "삼성동")

cond1 = df_legal_B['시군구명'] == sigungu_input
cond2 = df_legal_B['읍면동명'] == bdong_input
df_legal_B_input = df_legal_B[cond1&cond2]
st.dataframe(df_legal_B_input)

st.caption('--------', unsafe_allow_html=False)
st.subheader('■ 건축물대장정보검색')
st.markdown('2. 건축물 대장정보 서비스 드롭다운 선택')
st.markdown('3. 위 표에서 검색된 리스트에서 원하는 주소의 법정동기순구코드, 법정동읍면코드를 아래 입력 --------콤마(자릿점)제외--------')
st.markdown('4. 번, 지 입력 생략 후 동 전체 건물정보 크롤링 시 시간이 오래걸릴 수 있음')
# Collecting user input
ledger_type = st.selectbox("건축물 대장정보 서비스 선택", ("층별개요","기본개요", "총괄표제부", "표제부",  "부속지번", "전유공용면적", "오수정화시설", "주택가격", "전유부", "지역지구구역", "소유자"), index=0, key='ledger_type')
sigungu_code = st.text_input("법정동시군구 코드", "11680")
bdong_code = st.text_input("법정동읍면동 코드", "10500")
bun = st.text_input("번", "143")
ji = st.text_input("지", "20")

# Call API with user inputs
df = api.get_data(
    ledger_type=ledger_type,
    sigungu_code=sigungu_code,
    bdong_code=bdong_code,
    bun=bun,
    ji=ji
)

# Display DataFrame
st.markdown('5. CSV로 다운로드 하여 사용')
st.dataframe(df)