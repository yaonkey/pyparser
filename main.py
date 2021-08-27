#!/usr/bin/env python3
import time

import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from time import sleep

if os.name == "nt":
    SELENIUM_PATH = "assets\\geckodriver.exe"
elif os.name == 'posix':
    SELENIUM_PATH = "./assets/geckodriver"
else:
    SELENIUM_PATH = str(input("Enter path to Selenium: "))
FILENAME = "lesmastyle"
PRODUCT_TYPE = "Арка"

SITE_URLS = [
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
        "color": [],
        "material": [],
        "height": [],
        "width": [],
        "depth": [],
        "sku": [],
        "price": [],
    }

    def __init__(self, url: str == ""):
        if url != "":
            self.url = url
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')

    def run(self, url: str = ""):
        if url != "":
            self.url = url
        self.driver.get(self.url)
        sleep(7)
        html = self.driver.page_source
        self.soup = bs(html, "lxml")
        self.__process()
        # self.__save()

    def __save(self):
        csv_file = open("./data/" + FILENAME + ".csv", "a")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(self.processed_soup)

    def __process(self):
        product_div = self.soup.find('div', {"class", "home"})
        self.product["name"] = " ".join(f"{product_div.find('h2').get_text()}".split(" ")[0:2])
        self.product[
            'img'] = f"https://{FILENAME}.ru{[img.get('src') for img in product_div.find_all('img', {'class', 'img-fluid'})][0]}"  # .img-fluid[0]
        if self.url != "https://lesmastyle.ru/shop/arki/romanskaya/":
            self.product["color"] = [color.text.strip() for color in product_div.find_all('label', {
                'for': [mid['id'] for mid in
                        product_div.find_all("input", {"type": "radio", "class": "custom-control-input"})][3:]})]
            self.product['material'] = [material.text.strip() for material in product_div.find_all('label', {
                'for': [mid['id'] for mid in
                        product_div.find_all("input", {"type": "radio", "class": "custom-control-input"})][0:3]})]
        else:
            self.product["color"] = [color.text.strip() for color in product_div.find_all('label', {
                'for': [mid['id'] for mid in
                        product_div.find_all("input", {"type": "radio", "class": "custom-control-input"})][4:]})]
            self.product['material'] = [material.text.strip() for material in product_div.find_all('label', {
                'for': [mid['id'] for mid in
                        product_div.find_all("input", {"type": "radio", "class": "custom-control-input"})][0:4]})]

        # self.product["material"]
        self.product["height"] = [height.text.strip() for height in
                                  product_div.find("select", {"id": "property_height"}).find_all("option")]
        self.product["width"] = [width.text.strip() for width in
                                 product_div.find("select", {"id": "property_width"}).find_all("option")]
        self.product["depth"] = [depth.text.strip() for depth in
                                 product_div.find("select", {"id": "property_wall_thickness"}).find_all("option")]
        self.product["sku"] = product_div.find_all("span", {"class": "text-danger"})[0].get_text().split(" ")[1]
        self.product["price"] = ''.join([elem for elem in product_div.find_all("span", {"class": "text-danger"})[1].get_text().split(" ")[1] if elem != '\xa0'])

        print(self.product)
        return self.product

    def getPageFromUrl(self):
        return bs(requests.get(self.url).text, "lxml")

    def __del__(self):
        self.driver.quit()


delo = 1
pars = SiteParser(url="")
if delo == 1:
    for url in SITE_URLS:
        pars.run(url)
elif delo == 0:
    pars.run(SITE_URLS[0])
