import pandas as pd
import os
import numpy as np

# 법정동 코드 불러오기
legal_info_b = pd.read_excel('../data/KIKcd_B.20240208.xlsx', dtype= {'법정동코드':object})

#법정동 코드를 시군구코드와 동읍면 코드로 컬럼 분리 하기
legal_info_b['법정동시군구코드'] = legal_info_b['법정동코드'].str[:5]
legal_info_b['법정동읍면동코드'] = legal_info_b['법정동코드'].str[5:]

# 읍면동 없는 행 삭제후 인텍스 새로부여
legal_info_b = legal_info_b[['법정동코드',
                             '시도명',
                             '시군구명',
                             '읍면동명',
                             '동리명',
                             '법정동시군구코드',
                             '법정동읍면동코드']]

legal_info_b = legal_info_b[legal_info_b['법정동읍면동코드'] != '00000']
legal_info_b = legal_info_b.reset_index(drop=True)

#동리명에 NaN 인것을 빈칸으로 대치
legal_info_b = legal_info_b.where(pd.notnull(legal_info_b), " ")

#양쪽 공백이 있는경우 제거하는 전처리
legal_info_b['시도명'] = legal_info_b['시도명'].str.strip()
legal_info_b['시군구명'] = legal_info_b['시군구명'].str.strip()
legal_info_b['읍면동명'] = legal_info_b['읍면동명'].str.strip()
legal_info_b['동리명'] = legal_info_b['동리명'].str.strip()

legal_info_b['주소'] = legal_info_b['시도명'] + ' ' + \
      legal_info_b['시군구명'] + ' ' + \
          legal_info_b['읍면동명'] + ' ' + \
            legal_info_b['동리명']

legal_info_b['주소'] = legal_info_b['주소'].str.replace('  ',' ')
legal_info_b['주소'] = legal_info_b['주소'].str.strip()

legal_info_b.to_csv('../data/legal_info_b.csv')