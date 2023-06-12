import asyncio
from playwright.async_api import async_playwright, Browser
import os
from enum import Enum
from chlee.Common import Common
import time
 
'''
DB 컬럼명 정보
'''
class DataInfo(Enum):
    총전입 = "총전입 (명)"
    총전출 = "총전출 (명)"
    순이동 = "순이동 (명)"
    시도내이동시군구내 = "시도내이동-시군구내 (명)"
    시도내이동시군구간전입 = "시도내이동-시군구간 전입 (명)"
    시도내이동시군구간전출 = "시도내이동-시군구간 전출 (명)"
    시도간전입 = "시도간전입 (명)"
    시도간전출 = "시도간전출 (명)"
    
    
'''
한달 단위로 시군구별 이동자 수 데이터 수집 및 CSV 저장
페이지 조회기간 한계점 : 23.05 월에 데이터 조회 시 23.04 데이터 까지 밖에 없음. (예외처리)
'''
class Controller():
    '''
    _url : 시군구별 이동자수 수집 링크
    '''
    def __init__(self):
        self._url = '''https://kosis.kr/statHtml/statHtml.do?orgId=101&tblId=DT_1B26001_A01&conn_path=I2'''
        self._common = Common()
        self._folderName = "4_data"
        self._folderPath = os.path.join(*[os.getcwd(),self._folderName])
        self._common.MakeFolder(self._folderPath)
    
    def __del__(self):
        pass
    
    async def Run(self,_year:str,_month:str):
        try:
            _fileName = f'이동자수_{_year}_{_month}.csv'
            _filePath = os.path.join(self._folderPath,_fileName)
            _month = str(_month) if int(_month) > 9 else "0" + str(_month) 
            _selectDate = _year + _month
            if await self.Request(_filePath,_selectDate):
                self._common.ChangeEncoding(_filePath)
                return True
            else:
                return False
        except Exception as _ex:
            print("Run() Error : " , _ex)
            return False
    
    async def Request(self,_fileName:str,_selectDate:str):
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
                
                await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("button", name="조회설정").click()
                await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("tab", name="시점 시점").click()
                
                await _page.frame(name="iframe_centerMenu").get_by_role("combobox", name="시작 시점").select_option(_selectDate)
                await _page.frame(name="iframe_centerMenu").get_by_role("combobox", name="마지막 시점").select_option(_selectDate)
                
                await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("button", name="조회", exact=True).click()
                await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("button", name="다운로드").click()
                await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("radio", name="CSV").check()
                
                async with _page.expect_download() as download_info:
                    await _page.frame_locator("iframe[name=\"iframe_rightMenu\"]").frame_locator("iframe[name=\"iframe_centerMenu\"]").get_by_role("link", name="다운로드").click()
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
    asyncio.run(controller.Run("2023","4"))
    _end = time.time()
    print(f"수집 걸린 시간 {_end - _start: .5f} sec")