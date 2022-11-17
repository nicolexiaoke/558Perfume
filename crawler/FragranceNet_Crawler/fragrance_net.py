import os, sys
path = __file__
for _ in range(2):
    path = os.path.split(path)[0]
sys.path.append(path)

from Amazon.amazon import *
from modules import jsonl as parser
from modules.proj_os import *
from lxml import etree
from selenium import webdriver
from time import sleep

class CheckAntiCrawl:
    import pyautogui as pag

    def check(self):
        while (True):
            try:
                x,y = self.pag.locateCenterOnScreen("./pics/anti.png", confidence=0.98)
                print("Anti-crawler verification process detected.")
                print("waiting for manully handle.")
                sleep(0.25)
                input("Is it handled? (y/n):")
            except:
                break



class FragranceNet(PatchResult):
    def __init__(self, header: dict) -> None:
        super().__init__("https://www.fragrancenet.com", header)

    def __sroll_to_bottom(self, driver):
        height = driver.execute_script("return document.body.scrollHeight")
        count = 0
        while (count < height):
            count += 20
            driver.execute_script(f"window.scrollTo(0, {count});")
            sleep(0.05)

    def __patch_details(self, details):
        pass

    def get_result(self, driver, URL_Pateern, **kargs):
        pass

    def get_page_urls(self, driver, page_pattern: str, max_page: int= 30):
        pass

