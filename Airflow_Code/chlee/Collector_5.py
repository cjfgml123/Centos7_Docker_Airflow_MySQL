import requests
import xml.etree.ElementTree as ET
import pendulum
from chlee.Common import Common , ApartDealInfo

'''
- 데이터 수집 클래스
    - RestAPI 방식 사용
    - 파싱 처리 방식 : XML
    - ApartRun() 호출 시 수집 시작
    - 데이터 수집 후 CSV 파일 저장
    - 변수 설명 :
        - self._auth : 서비스 키
        - self._lawd_cdList : 경기도 지역권 번호 리스트 ex):성남시, 부천시 ...
        - self._url : Rest API 요청 URL
        - self._dataDict : 수집된 데이터 관리
        - self._common : 공통으로 쓰이는 메소드 관리 객체 ex) csv인코딩 변환, csv 저장, 등등
'''
class Controller():
    def __init__(self):
        self._auth = "ServiceKey"

        self._lawd_cdList = ['41131','41133','41135','41171','41173','41190','41281','41285','41287'] 
        self._url = f'''http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'''
        
        self._dataDict = {
            ApartDealInfo.거래가격.value : [],
            ApartDealInfo.건축년도.value : [],
            ApartDealInfo.매매년도.value : [],
            ApartDealInfo.매매월.value : [],
            ApartDealInfo.매매일.value : [],
            ApartDealInfo.법정동.value : [],
            ApartDealInfo.아파트명.value : [],
            ApartDealInfo.면적.value : [],
            ApartDealInfo.지번번호.value : [],
            ApartDealInfo.행정구역번호.value : [],
            ApartDealInfo.층.value : [],
            ApartDealInfo.년월.value : [],
            ApartDealInfo.수집시간.value : [],
        }
        self._common = Common()
        
    '''
    - 수집 시작 메소드(수집 후 CSV 저장) 지역코드 개수 만큼 Request 요청
    - 파라미터
        - _deal_ymd : 수집할 데이터 기간 : ex)201512
        - _fileName : csv파일 이름
    '''    
    def ApartRun(self,_deal_ymd:str,_fileName:str):
        for _lawd_cd in self._lawd_cdList:
            if not self.Request(_lawd_cd,_deal_ymd):
                return False
            self._common.DictToCSV(self._dataDict,_fileName)
        return True
        
    '''
    - 지역코드와 수집기간을 받아서 Rest API 요청
    - 파라미터
        - _lawd_cd : 지역코드
        - _deal_ymd : 수집할 데이터 기간
    '''
    def Request(self,_lawd_cd:str,_deal_ymd:str):      
        try:    
            _params ={'serviceKey' : self._auth, 'LAWD_CD' : _lawd_cd, 'DEAL_YMD' : _deal_ymd}
            _res = requests.get(self._url,params=_params)
            
            if _res.status_code != 200:
                return False
            
            _tree = ET.fromstring(_res.text)            
            if self.Parsing(_tree,_deal_ymd):
                return True
            else:
                return False
        except Exception as _ex: 
            print(_ex)
            return False    
    
    '''
    - XML 데이터 파싱
    - 파라미터
        - _tree : XML데이터 스크립트
    '''
    def Parsing(self,_tree,_deal_ymd:str):     
        try:
            _collTime = pendulum.now(tz="Asia/Seoul")
            _timeStr = f'{str(_collTime.hour)}:{str(_collTime.minute)}:{str(_collTime.second)}'
            for _item in _tree.iter('item'):
                self._dataDict[ApartDealInfo.거래가격.value].append(_item.find('거래금액').text.strip().replace(",",""))
                self._dataDict[ApartDealInfo.건축년도.value].append(_item.find('건축년도').text)
                self._dataDict[ApartDealInfo.매매년도.value].append(_item.find('년').text)
                self._dataDict[ApartDealInfo.매매월.value].append(_item.find('월').text)
                self._dataDict[ApartDealInfo.매매일.value].append(_item.find('일').text)
                self._dataDict[ApartDealInfo.법정동.value].append(_item.find('법정동').text)
                self._dataDict[ApartDealInfo.아파트명.value].append(_item.find('아파트').text)
                self._dataDict[ApartDealInfo.면적.value].append(_item.find('전용면적').text)
                self._dataDict[ApartDealInfo.지번번호.value].append(_item.find('지번').text)
                self._dataDict[ApartDealInfo.행정구역번호.value].append(_item.find('지역코드').text)
                self._dataDict[ApartDealInfo.층.value].append(_item.find('층').text)
                self._dataDict[ApartDealInfo.년월.value].append(_deal_ymd)
                self._dataDict[ApartDealInfo.수집시간.value].append(_timeStr)
            return True
        except AttributeError as _ex:
            print("Parsing() AttributeError 발생",_ex)
            return False
        except Exception as _ex: 
            print(_ex)  
            return False    
                   
if __name__ == "__main__":
    Controller()