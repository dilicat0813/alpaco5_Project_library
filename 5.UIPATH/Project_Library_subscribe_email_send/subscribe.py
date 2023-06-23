import pandas as pd
import re
import os

def subscribe_list():
    folder_path = r"C:\RPA\Library\Data"

    # 폴더가 존재하지 않으면 폴더를 생성합니다
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, "subscribe.csv")

    #기본 DB불러오기
    total = pd.read_csv("6.Subscribe_extract/data/total.csv", index_col=0) #경로/이름 설정
    subscribe = pd.read_csv("6.Subscribe_extract/data/subscribe.csv") #경로/이름 설정
    subscribe.drop_duplicates(subset="EMAIL", keep='last', inplace=True)
    subscribe.to_csv(file_path, index=False, encoding='utf-8-sig') #RPA 소스 파일 저장 #논리상 위치 여기가 맞음
    DT_Query = total[(total['MUMM_LON_HALFLIFE_CO'] >= 350) & (total['MUMM_LON_HALFLIFE_CO'] <= 6000)] #반감기 데이터 중 이상치 및 상위 5퍼센트 제거
    DT_Query = DT_Query[(DT_Query['LON_CO'] <= 6500)] #누적 대출수 상위 5퍼센트 제거

    DT_recommend = pd.DataFrame()

    for index, row in subscribe.iterrows():
        kdc_query = row['KDC']
        srchwrd_query = row['SRCHWRD']
        file_name = row['EMAIL']
        DT_Query1 = DT_Query[DT_Query['KDC_1'] == kdc_query]

        srchwrd = srchwrd_query
        
        try:
            srchwrd_list = re.findall(r'\w+', srchwrd)
        except:
            srchwrd_list = []
        
        if srchwrd:
            DT_Query2 = DT_Query1[
                DT_Query1['TITLE_NM'].str.contains('|'.join(srchwrd_list), regex=True) |
                DT_Query1['AUTHR_NM'].str.contains('|'.join(srchwrd_list), regex=True) |
                DT_Query1['PUBLISHER_NM'].str.contains('|'.join(srchwrd_list), regex=True) |
                DT_Query1['BOOK_INTRCN_CN'].str.contains('|'.join(srchwrd_list), regex=True) |
                DT_Query1['Combined'].str.contains('|'.join(srchwrd_list), regex=True)
            ]
            DT_Query2 = DT_Query2.drop_duplicates()
        
            if len(DT_Query2) > 0:
                DT_recommend = DT_Query2.sample(5)
            else:
                DT_recommend = DT_Query1.sample(5)
        else:
            DT_recommend = DT_Query1.sample(5)

        DT_recommend.drop(columns=['BOOK_MASTR_SEQ_NO', 'MUMM_LON_HALFLIFE_CO', 'MXMM_LON_HALFLIFE_CO', 'AVRG_LON_HALFLIFE_CO', 'BOOK_CO','ISBN_THIRTEEN_NO','SEQ_NO','ADTION_SMBL_NM','LON_CO','Combined', 'KDC_1', 'KDC_12', 'KDC_123'],axis=1, inplace=True)
        
        file_path = os.path.join(folder_path, f"{file_name}.csv")
        DT_recommend.to_csv(file_path, index=False, encoding='utf -8-sig') #RPA 소스 파일 저장

