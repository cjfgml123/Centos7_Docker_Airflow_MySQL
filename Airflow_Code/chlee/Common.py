import pandas as pd
import os
from enum import Enum

'''
- 적금 데이터 DB 컬럼 정보(Collector_1.py,DataQuery.py 에서 사용)
- DB 컬럼 이름 바뀔때 변경
'''
class SavingDataInfo(Enum):
    육개월 = "si_6"
    십이개월 = "si_12"
    이십사개월 = "si_24"
    삼십육개월 = "si_36"
    공시일 = "dcla_date"
    저축은행명 = "sb_nm"
    적금상품명 = "mndp_nm"
    기준일자 = "intr_date"
    지역 = "sido"
    채널명 = "category"
    적립형태 = "install_category"


'''
- 예금 데이터 DB 컬럼 정보 (Collector_1.py,DataQuery.py 에서 사용)
- DB 컬럼 이름 바뀔때 변경
'''
class DepositDataInfo(Enum):
    육단리 = "si_6"
    십이단리 = "si_12"
    이십사단리 = "si_24"
    삼십육단리 = "si_36"
    육복리 = "ci_6"
    십이복리 = "ci_12"
    이십사복리 = "ci_24"
    삼십육복리 = "ci_36"
    공시일 = "dcla_date"
    저축은행명 = "sb_nm"
    정기예금상품명 = "mndp_nm"
    기준일자 = "intr_date"
    시도 = "sido"
    채널구분명 = "category"
 
'''
 - 아파트 실거래 매매 데이터 DB 컬럼 정보(Collector_5.py,DataQuery.py 에서 사용)
 - DB 컬럼 이름 바뀔때 변경
'''
class ApartDealInfo(Enum):
    거래가격 = "price"
    건축년도 = "build_y"
    매매년도 = "year"
    매매월 = "month"
    매매일 = "day"
    법정동 = "dong"
    아파트명 = "apt_nm"
    면적 = "size"
    지번번호 = "jibun"
    행정구역번호 = "ji_code"
    층 = "floor"
    년월 = "ym"
    아이디 = "id"
    수집시간 = "collected_time"

'''
- 공통으로 사용되는 클래스
''' 
class Common():
    def __init__(self):
        pass
    
    def __del__(self):
        pass
    
    '''
    dict To CSV
    '''
    def DictToCSV(self,_dataDict:dict,_filePath:str):
        try:
            _dataDf = pd.DataFrame(_dataDict)
            #print(_dataDf.head())
            _dataDf.to_csv(os.path.join(_filePath),index=False)
        except Exception as _ex:
            print("DictToCSV Error : ", _ex)
    
    '''
    Dict 초기화
    '''
    def InitDict(_dataDict:dict):
        for _key in _dataDict:
            _dataDict[_key] = []
        return _dataDict 
    
    '''
    데이터 저장 폴더 생성
    '''
    def MakeFolder(self,_folderPath):
        if not os.path.exists(_folderPath):
            os.makedirs(_folderPath)
    
    '''
    encoding : ANSI -> utf-8 변경
    '''
    def ChangeEncoding(self,_filePath:str):
        try:
            _df = pd.read_csv(_filePath,encoding="ANSI")
            _df.to_csv(_filePath,encoding="utf-8",index=False)
        except Exception as _ex:
            print("ChangeEncoding Error() : " , _ex)