#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os

if os.name == "nt":
    SELENIUM_PATH = "assets\\geckodriver.exe"
elif os.name == 'posix':
    SELENIUM_PATH = "./assets/geckodriver"
FILENAME = "lesmastyle"
PRODUCT_TYPE = "Арка"

site_urls = [
    "https://lesmastyle.ru/shop/arki/ellada/",
    "https://lesmastyle.ru/shop/arki/britanskaya/",
    "https://lesmastyle.ru/shop/arki/valencia/",
    "https://lesmastyle.ru/shop/arki/kazanka/",
    "https://lesmastyle.ru/shop/arki/milano/",
    "https://lesmastyle.ru/shop/arki/palermo/",
    "https://lesmastyle.ru/shop/arki/romanskaya/",
    "https://lesmastyle.ru/shop/arki/ufimka/"
]


class SiteParser:
    product: dict = {
        "name": '',
        "img": '',
        "color": '',
        "material": '',
        "height": [],
        "width": [],
        "depth": [],
        "sku": '',
        "price": '',
    }

    def __init__(self, url: str):
        self.url = url

    def run(self):
        resp = requests.get(self.url)
        driver = webdriver.Firefox(executable_path=rf'{SELENIUM_PATH}')
        driver.get(self.url)
        html = driver.page_source
        self.soup = bs(html, "lxml")
        self.processed_soup = self.__process()
        # self.__save()

    def __save(self):
        csv_file = open("./data/" + FILENAME + ".csv", "a")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(self.processed_soup)

    def __process(self):
        self.product["name"] = f"{PRODUCT_TYPE} {self.soup.find('h1', {'class': 'header-img mb-3'}).get_text()}"
        # self.product["img"] = self.soup.find("div.cat-item__img.mb-4 a", {"data-fancybox": "shop-item-photo",
        #                                                                   "class": "d-block mb-3"}).get("href")
        print([img.get("src") for img in self.soup.find_all('img')])
        # self.product["img"] = [img for img.get('') in self.soup.find_all('a')]
        # self.product["color"] = self.soup.find("h4", {"class": "font-weight-bold"}).getText()
        self.product["material"] = self.soup.find()
        self.product["height"] = self.soup.find()
        self.product["width"] = self.soup.find()
        self.product["depth"] = self.soup.find()
        self.product["sku"] = self.soup.find()
        self.product["price"] = self.soup.find()
        print(self.product["name"])
        print(self.product["img"])
        # print(self.product["color"])
        return self.product

    def getPageFromUrl(self):
        return bs(requests.get(self.url).text, "lxml")


delo = 0
if delo == 1:
    for url in site_urls:
        pars = SiteParser(url)  # one element for testing
        pars.run()
elif delo == 0:
    pars = SiteParser(site_urls[0])  # one element for testing
    pars.run()
