from chlee.Common import SavingDataInfo , DepositDataInfo, ApartDealInfo
from chlee.MySql import MySql
import pandas as pd 

'''
- Table 생성 및 데이터 Insert 쿼리 처리 클래스
- DataQuery 객체 생성 시 DB 연결됨.
- DB 관련 처리 후 DisConnect() 사용 권장.
'''
class DataQuery:
    def __init__(self,_host:str,_port:int,_dbName:str,_user:str,_pw:str,_tableName:str):
        self._host = _host
        self._port = _port
        self._dbName = _dbName
        self._user = _user
        self._pw = _pw     
        self._tableName = _tableName
        self._conn = MySql(self._dbName,self._host,self._port,self._user,self._pw)
        
        if not self._conn.Connect():
            return 
        
    '''
    - Collector_1.py에서 수집한 적금 데이터 Insert 쿼리
    - 파라미터
        - _df : 수집한 적금 데이터 
    '''
    def InsertSavingDFToTable(self,_df:pd.DataFrame):
        _list = [tuple(_row) for _row in _df.values]
        _query = f'''INSERT INTO {self._tableName} ({SavingDataInfo.육개월.value},{SavingDataInfo.십이개월.value},
        {SavingDataInfo.이십사개월.value},{SavingDataInfo.삼십육개월.value},{SavingDataInfo.공시일.value},{SavingDataInfo.저축은행명.value},
        {SavingDataInfo.적금상품명.value},{SavingDataInfo.기준일자.value},{SavingDataInfo.지역.value},{SavingDataInfo.채널명.value},
        {SavingDataInfo.적립형태.value}) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''           
        self._conn.InsertBigData(_query,_list)
    
    '''
    - Collector_1.py에서 수집한 예금 데이터 Insert 쿼리
    - 파라미터
        - _df : 수집한 예금 데이터
    '''
    def InsertDepositDFToTable(self,_df:pd.DataFrame):
        _list = [tuple(_row) for _row in _df.values]
        _query = f'''INSERT INTO {self._tableName} ({DepositDataInfo.육단리.value},{DepositDataInfo.십이단리.value},
        {DepositDataInfo.이십사단리.value},{DepositDataInfo.삼십육단리.value},{DepositDataInfo.육복리.value},{DepositDataInfo.십이복리.value},
        {DepositDataInfo.이십사복리.value},{DepositDataInfo.삼십육복리.value},{DepositDataInfo.공시일.value},{DepositDataInfo.저축은행명.value},
        {DepositDataInfo.정기예금상품명.value},{DepositDataInfo.기준일자.value},{DepositDataInfo.시도.value},{DepositDataInfo.채널구분명.value}) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''           
        self._conn.InsertBigData(_query,_list)
    
    '''
     - Collector_1.py에서 수집한 적금 테이블 Create 쿼리
    '''
    def CreateTable_SavingData(self):
        _query = f'''CREATE TABLE IF NOT EXISTS {self._tableName} (
            id INT NOT NULL AUTO_INCREMENT,
            {SavingDataInfo.기준일자.value} DATE NOT NULL,
            {SavingDataInfo.공시일.value} DATE, #데이터에'-' 값 있음.
            {SavingDataInfo.적금상품명.value} VARCHAR(100) NOT NULL,
            {SavingDataInfo.저축은행명.value} VARCHAR(10),
            {SavingDataInfo.육개월.value} FLOAT,
            {SavingDataInfo.십이개월.value} FLOAT,
            {SavingDataInfo.이십사개월.value} FLOAT,
            {SavingDataInfo.삼십육개월.value} FLOAT,
            {SavingDataInfo.지역.value} VARCHAR(10),
            {SavingDataInfo.채널명.value} VARCHAR(10),
            {SavingDataInfo.적립형태.value} VARCHAR(10),
            PRIMARY KEY (id)
            )'''
        self._conn.Create(_query)

    '''
    - Collector_1.py에서 수집한 예금 테이블 Create 쿼리
    '''
    def CreateTable_DepositData(self):
        _query = f'''CREATE TABLE IF NOT EXISTS {self._tableName} (
            id INT NOT NULL AUTO_INCREMENT,
            {DepositDataInfo.기준일자.value} DATE NOT NULL,
            {DepositDataInfo.공시일.value} DATE, #데이터에'-' 값 있음.
            {DepositDataInfo.정기예금상품명.value} VARCHAR(100) NOT NULL,
            {DepositDataInfo.저축은행명.value} VARCHAR(10),
            {DepositDataInfo.육단리.value} FLOAT,
            {DepositDataInfo.십이단리.value} FLOAT,
            {DepositDataInfo.이십사단리.value} FLOAT,
            {DepositDataInfo.삼십육단리.value} FLOAT,
            {DepositDataInfo.육복리.value} FLOAT,
            {DepositDataInfo.십이복리.value} FLOAT,
            {DepositDataInfo.이십사복리.value} FLOAT,
            {DepositDataInfo.삼십육복리.value} FLOAT,
            {DepositDataInfo.시도.value} VARCHAR(10),
            {DepositDataInfo.채널구분명.value} VARCHAR(10),
            PRIMARY KEY (id)
            )'''
        self._conn.Create(_query)
    
    '''
    - Collector_5.py 에서 수집한 아파트 실거래 매매 Insert 쿼리
    - 중복 데이터 UPDATE : 수집시간만 UPDATE함.
    - 파라미터:
        - _df : 수집한 아파트 실거래 매매 데이터
    '''
    def InsertApartDFToTable(self,_df:pd.DataFrame):
        _list = [tuple(_row) for _row in _df.values]
        _query = f'''INSERT INTO {self._tableName} ({ApartDealInfo.거래가격.value},{ApartDealInfo.건축년도.value},
        {ApartDealInfo.매매년도.value},{ApartDealInfo.매매월.value},{ApartDealInfo.매매일.value},{ApartDealInfo.법정동.value},
        {ApartDealInfo.아파트명.value},{ApartDealInfo.면적.value},{ApartDealInfo.지번번호.value},{ApartDealInfo.행정구역번호.value},
        {ApartDealInfo.층.value},{ApartDealInfo.년월.value},{ApartDealInfo.수집시간.value}) 
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
        ON DUPLICATE KEY UPDATE
            {ApartDealInfo.수집시간.value} = VALUES({ApartDealInfo.수집시간.value})'''           
        self._conn.InsertBigData(_query,_list)
    
    '''
    - Collector_5.py에서 수집한 아파트 실거래 매매 테이블 Create 쿼리
    '''
    def CreateTable_ApartData(self):
        _query = f'''CREATE TABLE IF NOT EXISTS {self._tableName} (
            {ApartDealInfo.매매년도.value} INT NOT NULL,
            {ApartDealInfo.매매월.value} INT NOT NULL,
            {ApartDealInfo.매매일.value} INT NOT NULL,
            {ApartDealInfo.지번번호.value} VARCHAR(20) NOT NULL, 
            {ApartDealInfo.층.value} INT NOT NULL,
            {ApartDealInfo.년월.value} VARCHAR(10) NOT NULL,
            {ApartDealInfo.거래가격.value} INT,
            {ApartDealInfo.건축년도.value} INT,
            {ApartDealInfo.법정동.value} VARCHAR(10),
            {ApartDealInfo.아파트명.value} VARCHAR(50),
            {ApartDealInfo.면적.value} FLOAT,
            {ApartDealInfo.행정구역번호.value} INT,
            {ApartDealInfo.수집시간.value} VARCHAR(10),
            PRIMARY KEY ({ApartDealInfo.매매년도.value},{ApartDealInfo.매매월.value},{ApartDealInfo.매매일.value}
            ,{ApartDealInfo.지번번호.value},{ApartDealInfo.층.value},{ApartDealInfo.년월.value})
            )'''
        self._conn.Create(_query)
    
    '''
    - DB 연결 종료 메소드
    '''
    def DisConnect(self):
        self._conn.DisConnect()