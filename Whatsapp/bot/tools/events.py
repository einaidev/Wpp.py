"""Events Returns
Here was all the events, whare hendled
"""

from .clasesHtml import *
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup as bs4

class Message:
    def __init__(self, element):
        self.name = element.find_next("span", class_=messageguildname_class)["title"]
        self.channel.name = self.name
        self.message.content =  selement.find_next("span", class_=message_class)["title"]
        #self.message.author = self.element.find_next("span", class_ = author_class).text

        #print("{0} {1}".format(self.message.author, self.message.content))
    
    channel = type('C', (object,), {})
    message = type('C', (object,), {})

class BotOnline():
    def __init__(self, element, driver):
        self.user.thumbnail = element.find("img", class_= botuserImage_class)["src"]
        driver.find_element(By.XPATH, "//div[@aria-label={0!r}]".format(optionsbutton_aria_label)).click()
        time.sleep(1)

        driver.find_elements(By.XPATH, "//div[@aria-label='{0}']".format(configbtn_aria_label ))[0].click()

        time.sleep(1)
        source = driver.page_source
        sup = bs4(source, "html.parser")

        self.user.username = sup.find("span", class_=username_class)["title"]
        self.user.description = sup.find("span", class_=description_class)["title"]

        driver.find_element(By.XPATH, "//button[@aria-label={0!r}]".format(back_btn_aria_label)).click()
        time.sleep(1)
    user = type('C', (object,), {})