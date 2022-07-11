"""Events Returns
Here was all the events, whare hendled
"""

from .clasesHtml import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time,re
import unicodedata
from bs4 import BeautifulSoup as bs4

class Message:
    def __init__(self, element, driver):
        self.name = element.find_previous("span", class_ = messageguildname_class, dir = "auto", title = re.compile(".*"))["title"]
        self.channel.name = unicodedata.normalize("NFKD", self.name)
        self.message.content =  element.find_previous("span", class_=message_class, title = re.compile(".*"))["title"]
        self.channel.thumbnail = element.find_previous("img", class_=chatimage_class, draggable="false", style = "visibility: visible;")["src"]

        title = self.channel.name
        try:
            driver.find_element(By.XPATH, "//span[@title='{0}']".format(title)).click()
        except:
            driver.find_element(By.XPATH, "//span[@title='{0}']".format(self.name)).click()
        time.sleep(1)

        try:
            el = driver.find_element(By.XPATH, "//div[@class='{0}']//span[@title={1!r} and @class={2!r}]".format("_21nHd", title, userinfo_class))
            act = ActionChains(driver)
            act.move_to_element(el).click()
        except:
            el = driver.find_element(By.XPATH, "//div[@class='{0}']//span[@title={1!r} and @class={2!r}]".format("_21nHd", self.name, userinfo_class))
            act = ActionChains(driver)
            act.move_to_element(el).click()
        
        time.sleep(1)
        sup = bs4(driver.page_source, "html.parser")
        driver.save_screenshot("aaaa.png")

        if sup.find_next("h1", class_="", string="Dados do contato", style = "font-size: inherit;"):
            self.channel.type = 'contact'
            self.channel.number = sup.find_next("span", class_=usernumber_class).text
            self.channel.bio = sup.find_next("span", class_=userbio_class)["title"]
        else:
            self.channel.type = "group"
            self.channel.createdAt = {
                "per": sup.find_next("span", class_=goupdatecreated_class).text.split(" ")[3],
                "date": sup.find_next("span", class_=goupdatecreated_class).text.split(" ")[6],
                "hour": sup.find_next("span", class_=goupdatecreated_class).text.split(" ")[-1],
            }
        time.sleep(4)
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