import asyncio
from playwright.async_api import async_playwright, Browser, Page, TimeoutError as PlaywrightTimeoutError
from chlee.Common import Common,SavingDataInfo,DepositDataInfo
import time

'''
- 데이터 수집 클래스
    - 크롤링 방식 사용
    - 파싱 처리 방식 : playwright 라이브러리 사용, 비동기 방식
    - DepositRun() : 예금 데이터 수집 시작 메소드
    - SavingRun() : 적금 데이터 수집 시작 메소드
    - 데이터 수집 후 CSV 파일 저장
    - 변수 설명 :
        - self._sido : 수집 지역
        - self._depositUrl : 예금 데이터 수집할 URL
        - self.savingUrl : 적금 데이터 수집할 URL 
        - self._categoryDict : 카테고리별 데이터 수집해야함. 예금,적금 데이터 수집에 사용
        - self._install_cateDict : 적금 데이터 수집에만 사용 , 적립 종류
        - self._common : 공통으로 쓰이는 메소드 관리 객체 ex) csv인코딩 변환, csv 저장, 등등
'''
class Controller():
    def __init__(self):
        self._common = Common()
        self._sido = "경기"
        
        # 데이터 수집 URL
        self._depositUrl = "https://www.fsb.or.kr/ratedepo_0100.act?ETC_YN=Y";
        self._savingUrl = "https://www.fsb.or.kr/rateinst_0100.act?ETC_YN=Y";
        
        self._categoryDict:dict = {"대면":"chk02",
                             "인터넷":"chk03",
                             "스마트폰":"chk04"}
        
        self._install_cateDict:dict = {"정액적립식":"1",
                     "자유적립식":"2"}
        
    def __del__(self):
        pass 
    
    '''
    - 카테고리별 예금 데이터 수집 후 _dataDict에 넣고 CSV로 저장
    - 파라미터:
        - _fileName : CSV 파일이름
        - _year : 수집할 데이터 년도 ex) 2023
        - _month : 수집할 데이터 월 ex) 06
        - _day : 수집할 데이터 일 ex) 09
    '''
    async def DepositRun(self,_fileName:str,_year:str,_month:str,_day:str):
        try:
            _dataDict =  {
                        DepositDataInfo.육단리.value : [],
                        DepositDataInfo.십이단리.value : [],
                        DepositDataInfo.이십사단리.value : [],
                        DepositDataInfo.삼십육단리.value : [],
                        DepositDataInfo.육복리.value : [],
                        DepositDataInfo.십이복리.value : [],
                        DepositDataInfo.이십사복리.value : [],
                        DepositDataInfo.삼십육복리.value : [],
                        DepositDataInfo.공시일.value : [],
                        DepositDataInfo.저축은행명.value : [],
                        DepositDataInfo.정기예금상품명.value : [],
                        DepositDataInfo.기준일자.value : [],
                        DepositDataInfo.시도.value : [],
                        DepositDataInfo.채널구분명.value : []
                    }
            
            for _key in self._categoryDict: 
                if not await self.DepositRequest(_year,_month,_day,_dataDict,_key):
                    print(f'''DepositRun() Error : {_key} Selector Collect.''')
                    return False
                
            self._common.DictToCSV(_dataDict,_fileName)   
            return True 
        except Exception as _ex:
            print("DepositRun() Error : ", _ex)
            return False
    
    '''
    - 카테고리별, 적금방식별 적금 데이터 수집 후 _dataDict에 넣고 CSV로 저장
    - 파라미터:
        - _fileName : CSV 파일이름
        - _year : 수집할 데이터 년도 ex) 2023
        - _month : 수집할 데이터 월 ex) 06
        - _day : 수집할 데이터 일 ex) 09
    '''
    async def SavingRun(self,_fileName:str,_year:str,_month:str,_day:str):
        try:
            _dataDict = {
                SavingDataInfo.육개월.value : [],
                SavingDataInfo.십이개월.value : [],
                SavingDataInfo.이십사개월.value : [],
                SavingDataInfo.삼십육개월.value : [],
                SavingDataInfo.공시일.value : [],
                SavingDataInfo.저축은행명.value : [],
                SavingDataInfo.적금상품명.value : [],
                SavingDataInfo.기준일자.value : [],
                SavingDataInfo.지역.value : [],
                SavingDataInfo.채널명.value : [],
                SavingDataInfo.적립형태.value : [],
            } 
            
            for _key in self._categoryDict:
                for _installCateKey  in self._install_cateDict:
                    if not await self.SavingRequest(_year,_month,_day,_dataDict,_key,_installCateKey):
                        print(f'''SavingRun() Error : {_key} Selector Collect.''')
                        return False
            
            self._common.DictToCSV(_dataDict,_fileName)
            return True
        except Exception as _ex:
            print("SavingRun() Error : ", _ex)
            return False
    
    '''
    - 적금 데이터 수집 메소드
    - 파라미터 대로 페이지 내에서 값을 설정 후 클릭 후에 데이터 파싱
    - headless : False 일때 코드 실행 시 페이지 나오면서 디버깅 가능 
    - playwright 브러우저 : chromium 에서 데이터 수집 안됨. 파이어폭스나 webkit 사용(적금 페이지만 이럼.)
    - 파라미터 
        - _year : 수집할 데이터 조회 년
        - _month : 수집할 데이터 조회 월
        - _day : 수집할 데이터 조회 일
        - _dataDict : 수집된 데이터 임시 저장 -> 후에 df -> csv로 전환
        - _key : 카테고리별 key(영업점,인터넷,스마트폰)
        - _installCateKey  : 적금 방식(정액적립식,자유적립식)
    '''
    async def SavingRequest(self,_year:str,_month:str,_day:str,_dataDict:dict,_key:str,_installCateKey:str):
        try:
            async with async_playwright() as _playWright:
                _browser: Browser = await _playWright.webkit.launch(
                    headless=True
                )
                _context = await _browser.new_context()
                _page = await _context.new_page()
                
                await _page.goto(self._savingUrl) 
                await _page.wait_for_load_state("load")
                await _page.wait_for_selector(selector='#instTbody > tr:nth-child(1) > td.table-detail',timeout=30000,state='attached')
                await _page.get_by_role("combobox", name="지역").select_option("YN_Kyungki") # 경기 지역 검색
                
                await _page.eval_on_selector(
                    'select#selectYear',
                    'el => el.value = "' + _year + '"'
                )
                await _page.eval_on_selector(
                    'select#selectMonth',
                    'el => el.value = "' + _month + '"'
                )
                await _page.eval_on_selector(
                    'select#selectDay',
                    'el => el.value = "' + _day + '"'
                )
                
                await _page.click(f'''label[for="{self._categoryDict[_key]}"]''')
                
                await _page.get_by_role("combobox", name="적립식").select_option(self._install_cateDict[_installCateKey])
                
                await _page.eval_on_selector('#searchBtn', 'btn => btn.click()')
                
                await _page.wait_for_load_state('load')
                await _page.wait_for_timeout(2000)
                await _page.wait_for_selector(selector='#instTbody > tr:nth-child(1) > td.table-detail',timeout=20000,state='attached')

                if await self.SavingParsingData(_page,_dataDict,_key,_installCateKey):
                    print(f'적금 {_key} {_installCateKey} Data {_year}년 {_month} 월 {_day}일 데이터 수집 완료')
                    await _browser.close()
                    await _page.close()
                    return True
                else:
                    print(f'적금 {_key} {_installCateKey} Data {_year}년 {_month} 월 {_day}일 데이터 수집 실패ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
                    await _browser.close()
                    await _page.close()
                    return False
        except PlaywrightTimeoutError as _ex:
            print("SavingRequest() Timeout Error ", _ex)
            return False
        except Exception as _ex :
            print("SavingRequest() Error : " , _ex)
            return False            
    
    '''
    - 예금 데이터 수집 메소드
    - 파라미터 대로 페이지 내에서 값을 설정 후 클릭 후에 데이터 파싱
    - headless : False 일때 코드 실행 시 페이지 나오면서 디버깅 가능 
     - 파라미터 
        - _year : 수집할 데이터 조회 년
        - _month : 수집할 데이터 조회 월
        - _day : 수집할 데이터 조회 일
        - _dataDict : 수집된 데이터 임시 저장 -> 후에 df -> csv로 전환
        - _key : 카테고리별 key(영업점,인터넷,스마트폰)
        
    '''
    async def DepositRequest(self,_year:str,_month:str,_day:str,_dataDict:dict,_key:str):
        try:
            async with async_playwright() as _playWright:
                _browser: Browser = await _playWright.chromium.launch(
                    #headless=False
                    headless=True
                )
                _page = await _browser.new_page()
                
                # headless : False 할때 주석 풀어야함.
                #await _page.set_viewport_size({"width":1800,"height":1800})
                await _page.goto(self._depositUrl) 
                
                await _page.wait_for_load_state("load")
                
                await _page.eval_on_selector('#searchBtn', 'btn => btn.click()')
                await _page.wait_for_selector(selector='#depoTbody > tr:nth-child(1) > td.table-detail',timeout=20000,state='attached')
                await _page.get_by_role("combobox", name="지역").select_option("YN_Kyungki") # 경기 지역 검색
                
                await _page.eval_on_selector(
                    'select#selectYear',
                    'el => el.value = "' + _year + '"'
                )
                await _page.eval_on_selector(
                    'select#selectMonth',
                    'el => el.value = "' + _month + '"'
                )
                await _page.eval_on_selector(
                    'select#selectDay',
                    'el => el.value = "' + _day + '"'
                )
                
                await _page.click('label[for="chk01"]') #전체 선택
                await _page.click(f'''label[for="{self._categoryDict[_key]}"]''')
                
                await _page.eval_on_selector('#searchBtn', 'btn => btn.click()')
                
                await _page.wait_for_timeout(2000)
                await _page.wait_for_load_state('load')

                if await self.DepositParsingRawData(_page,_dataDict,_key):
                    print(f'예금 {_key} Data {_year}년 {_month} 월 {_day}일 데이터 수집 완료')
                    await _browser.close()
                    await _page.close()
                    return True
                else:
                    print(f'예금 {_key} Data {_year}년 {_month} 월 {_day}일 데이터 수집 실패ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
                    await _browser.close()
                    await _page.close()
                    return False
        except PlaywrightTimeoutError as _ex:
            print("DepositRequest() Timeout Error ", _ex)
            return False
        except Exception as _ex :
            print("DepositRequest() Error : " , _ex)
            return False            
    
    '''
    - 페이지내에서 적금 데이터 파싱
    - 파라미터 :
        - _page : 파싱할 페이지 객체
        - _dataDict : 수집된 데이터 임시 저장 -> 후에 df -> csv로 전환
        - _key : 카테고리별 key(영업점,인터넷,스마트폰)
        - _installCateKey  : 적금 방식(정액적립식,자유적립식)
    '''
    async def SavingParsingData(self,_page:Page,_dataDict:dict,_key:str,_installCateKey:str):
        try:
            _intr_date = await _page.text_content(selector='#viewDate')
            _trs = await _page.eval_on_selector_all("#instTbody tr:not(.tr-info)",
                "trs => trs.map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim()))")
            for _tr in _trs:
                _dataDict[SavingDataInfo.기준일자.value].append(_intr_date.replace('.','-'))
                _dataDict[SavingDataInfo.공시일.value].append(_tr[5].replace('.','-'))
                _bankNameStr = _tr[0].replace("상세보기","")
                _bankNameStr = _bankNameStr[0:len(_bankNameStr)//2]
                _bankNameList = _bankNameStr.split("[")[1].split("]") 
                _dataDict[SavingDataInfo.저축은행명.value].append(_bankNameList[0])
                _dataDict[SavingDataInfo.적금상품명.value].append(_bankNameList[1].strip())
                _dataDict[SavingDataInfo.육개월.value].append(_tr[1])
                _dataDict[SavingDataInfo.십이개월.value].append(_tr[2])
                _dataDict[SavingDataInfo.이십사개월.value].append(_tr[3])
                _dataDict[SavingDataInfo.삼십육개월.value].append(_tr[4])
                _dataDict[SavingDataInfo.적립형태.value].append(_installCateKey)
                _dataDict[SavingDataInfo.지역.value].append(self._sido)
                _dataDict[SavingDataInfo.채널명.value].append(_key)
            return True
        except PlaywrightTimeoutError as _ex:
            print("SavingParsingData() Timeout Error() ", _ex)
            return False
        except Exception as _ex:
            print("SavingParsingData() Error : ", _ex)
            return False
    
    '''
    - 페이지내에서 예금 데이터 파싱
    - 파라미터 :
        - _page : 파싱할 페이지 객체
        - _dataDict : 수집된 데이터 임시 저장 -> 후에 df -> csv로 전환
        - _key : 카테고리별 key(영업점,인터넷,스마트폰)
    '''
    async def DepositParsingRawData(self, _page: Page,_dataDict:dict,_key:str):
        try:
            _intr_date = await _page.text_content(selector='#viewDate')
            _trs = await _page.eval_on_selector_all("#depoTbody tr:not(.tr-info)",
                "trs => trs.map(tr => Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim()))")
            for _tr in _trs:
                _dataDict[DepositDataInfo.기준일자.value].append(_intr_date.replace('.','-'))
                _dataDict[DepositDataInfo.공시일.value].append(_tr[9].replace('.','-'))
                _bankNameStr = _tr[0].replace("상세보기","")
                _bankNameStr = _bankNameStr[0:len(_bankNameStr)//2]
                _bankNameList = _bankNameStr.split("[")[1].split("]") 
                _dataDict[DepositDataInfo.저축은행명.value].append(_bankNameList[0])
                _dataDict[DepositDataInfo.정기예금상품명.value].append(_bankNameList[1].strip())
                _dataDict[DepositDataInfo.육단리.value].append(_tr[1])
                _dataDict[DepositDataInfo.십이단리.value].append(_tr[2])
                _dataDict[DepositDataInfo.이십사단리.value].append(_tr[3])
                _dataDict[DepositDataInfo.삼십육단리.value].append(_tr[4])
                _dataDict[DepositDataInfo.육복리.value].append(_tr[5])
                _dataDict[DepositDataInfo.십이복리.value].append(_tr[6])
                _dataDict[DepositDataInfo.이십사복리.value].append(_tr[7])
                _dataDict[DepositDataInfo.삼십육복리.value].append(_tr[8])
                _dataDict[DepositDataInfo.시도.value].append(self._sido)
                _dataDict[DepositDataInfo.채널구분명.value].append(_key)
            return True
        except PlaywrightTimeoutError as _ex:
            print("DepositParsingRawData() Timeout Error ", _ex)
            return False
        except Exception as _ex:
            print("DepositParsingRawData Error : ", _ex)
            return False
    
    
if __name__ == "__main__":
    _start = time.time()
    controller = Controller()
    #asyncio.run(controller.DepositRun())
    asyncio.run(controller.SavingRun())
    
    _end = time.time()
    print(f"수집 걸린 시간 {_end - _start: .5f} sec")