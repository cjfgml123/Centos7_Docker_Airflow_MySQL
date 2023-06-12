import asyncio
from playwright.async_api import async_playwright, Browser
from enum import Enum
import os
import time
from chlee.Common import Common
'''
DB 컬럼명 정보
'''
class DataInfo(Enum):
    시군명 = "시군명"
    기준년월 = "기준년월"
    월별카드발행수량 = "월별카드발행수량(건)"
    월별카드충전액 = "월별카드충전액(천원)"
    월별카드사용액 = "월별카드사용액(천원)"
    월별모바일상품권이용등록자수 = "월별모바일상품권이용등록자수(명)"
    월별모바일충전액 = "월별모바일충전액(천원)"
    월별모바일사용액 = "월별모바일사용액(천원)"
    월별지류상품권판매액 = "월별지류상품권판매액(천원)"
    월별지류상품권회수액 = "월별지류상품권회수액(천원)"


class Controller():
    '''
    _url : 지역화폐발행 및 이용현황
    _folderName : 데이터 저장 폴더명
    '''
    def __init__(self):
        self._url = '''https://data.gg.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection
                        =&infId=6FEDD6KGEJWYCY2G15OY29527318&infSeq=1&order=&loc=&searchWord=경기지역화폐'''
        self._common = Common()
        self._folderName = "3_data"
        self._folderPath = os.path.join(*[os.getcwd(),self._folderName])
        self._common.MakeFolder(self._folderPath)
    
    def __del__(self):
        pass
    
    async def Run(self,_year:str,_month:str):
        try:
            _fileName = f'지역화폐_{_year}_{_month}.csv'
            _filePath = os.path.join(self._folderPath,_fileName)
            if await self.Request(_filePath):
                self._common.ChangeEncoding(_filePath)
                print(f'{_fileName} 저장 완료')
                return True
            else:
                return False
        except Exception as _ex:
            print("Run() Error : " , _ex)
            return False
        
            
    async def Request(self,_fileName:str):
        try:
            async with async_playwright() as _playWright:
                _browser: Browser = await _playWright.chromium.launch(
                    #headless=False
                    headless=True
                )
                _page = await _browser.new_page()
                #await _page.set_viewport_size({"width":1600,"height":1300})
                await _page.goto(self._url) 
                
                await _page.wait_for_load_state("load")
                await _page.click(selector="#sheet-csv-button")
                input_element = await _page.query_selector('input#dsUsePurpsCd_U01')
                await input_element.click()

                async with _page.expect_download() as download_info:
                    await _page.click('button#btnUtilPurpConf', force=True)
                _download = await download_info.value
                
                await _download.save_as(_fileName)
                
                await _browser.close()
                await _page.close()
            return True
        except Exception as _ex:
            print("Request() Error : ", _ex)
            return False        
        
if __name__ == "__main__":
    _start = time.time()
    controller = Controller()
    asyncio.run(controller.Run("2023","05"))
    _end = time.time()
    print(f"수집 걸린 시간 {_end - _start: .5f} sec")