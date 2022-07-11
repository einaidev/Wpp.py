"""
MIT License

Copyright (c) 2022 Einai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import re
import time
import asyncio
import platform
import qrcode_terminal as qrcodeShow
import _thread
import signal
from bs4 import BeautifulSoup as bs4

from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO
import base64

from selenium.webdriver.chrome.service import Service

import selenium
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

from .errors.errorHandling import *
from .errors import *
from .tools import *

import warnings

__WebDriverVersion__ = "103.0.5060.53"

class Client():
    def __init__(
        self,
        prefix:str,
        ever_connection:bool,
        location:str
    ):
        if ever_connection:
            opts.add_argument("--user-data-dir={0}".format(location+"Data" if location.endswith("/") else location))
        try:
            if platform.system() == "Windows":
                self.driver = webdriver.Chrome(options=opts,service=Service("./selenium/webdriver/chromedriver.exe"))
            else:
                self.driver = webdriver.Chrome(options=opts,service=Service("./selenium/webdriver/chromedriver"))
        except Exception as e:
            Handling(e, version=__WebDriverVersion__)

        self._listners = {}
        self._listners["message"] = []
        self._listners["ready"] = []

        self.validArgs_events={}
        self.validArgs_events["ready"] = {}

        self.valid_events = ["message", "ready"]
        def signalHand(signal,frame):
            print("Stoping")
            self.driver.close()
            self.driver.quit()
            exit()
        signal.signal(signal.SIGINT, signalHand)
        self.ever_connection = ever_connection
        self.location = location
        self.loop = asyncio.get_event_loop()
    def _isTitleMatching(self):
        return True if self.driver.title == "WhatsApp" else False

    def isSeed(self,element):
        if "mensagens não lidas" in element.find_next("span",class_=count_class)["aria-label"]:
            return True
        elif "mensagem não lida" in element.find_next("span",class_=count_class)["aria-label"]:
            return True
        else:
            return False

    async def _listner(self):
        while True:
            sup = bs4(self.driver.page_source, "html.parser")
            panel = sup.findAll("span",class_=count_class)
            for i in panel:
                def e():
                    title = i.find_previous("span", class_ = messageguildname_class, dir = "auto", title = re.compile(".*"))["title"]
                    valid_msg_arg = {"message": Message(i, self.driver)}
                    for event in self._listners["message"]:
                        pass
                        event["name"](*tuple([ valid_msg_arg[x] if x in valid_msg_arg else None for x in event["args"] ]))

                _thread.start_new_thread(e, ())
                await asyncio.sleep(.5)
    def run(self):
        """run
        your bot was be start here.
        """ 
        self.driver.get("https://web.whatsapp.com/")

        self._is_complete = False
        self.allready_logged = False
        l=self.location

        @CatchErros(self.driver)  
        def _wait_login():
            try:
                qrold = self.driver.find_element(By.CLASS_NAME, qrcode_class).screenshot_as_base64
                qrcodeShow.draw(decode(Image.open(BytesIO(base64.b64decode(qrold))))[0].data)
            except:
                self.allready_logged = True
                self._is_complete = True
                return

            if not self.allready_logged:
                while not self._is_complete:
                    try:
                        qr = self.driver.find_element(By.CLASS_NAME, qrcode_class).screenshot_as_base64
                        if not qrold == qr:
                            decode_data = decode(Image.open(BytesIO(base64.b64decode(qr))))[0].data
                            qrcodeShow.draw(decode_data)                    
                    except:
                        self._is_complete = True
                        break       

        @AsyncCatchErros(self.driver)
        async def _wait_loading():
            _loaded = False
            while not _loaded:
                if self.driver.find_elements(By.CLASS_NAME, wellcome_class).__len__() > 0:
                    break
                await asyncio.sleep(0.05)

        time.sleep(2)
        @CatchErros(driver)        
        def Complete():
            if self._is_complete:
                generalElement = bs4(self.driver.page_source, "html.parser")
                validArgs = {"user": BotOnline(generalElement, self.driver)}
                if not self._listners["ready"].__len__() == 0:
                    for event in self._listners["ready"]:
                        event["name"](*tuple([ validArgs[x] if x in validArgs else None for x in event["args"] ]))
                async_error_resolve(self._listner,self.driver)


        self.driver.close()
        self.driver.quit()
        
    def event(self,type):
        """Events
        this function execute each function in which it has that function as decorator,
        ex: def foo(args): ..., if the function above has the event decorator, it will be executed

        Events:
            ready: when this argument is passed to the decorator, each function receives some arguments.
                Arguments: `user`,
                    * thumbnail: URL. logged user avatar url.
                    * username: STR. logged user username.
                    * description STR. logged user description


        """

        if not type in self.valid_events: raise InvalidEvent("{0} Is a invalid event".format(type))
        def decorator(f):
            self._listners[type].append({"name": f, "args":[i for i in f.__code__.co_varnames]})
            return f
        return decorator