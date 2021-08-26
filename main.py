#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

FILENAME = "lesmastyle"

site_urls = [
    "https://lesmastyle.ru/shop/arki/ellada/",
    "https://lesmastyle.ru/shop/arki/britanskaya/",
    "https://lesmastyle.ru/shop/arki/valencia/",
    "https://lesmastyle.ru/shop/arki/kazanka/",
    "https://lesmastyle.ru/shop/arki/milano/",
    "https://lesmastyle.ru/shop/arki/palermo/",
    "https://lesmastyle.ru/shop/arki/romanskay/",
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
        soup = bs(resp.text, "lxml")
        print(soup)
        self.processed_soup = self.__process(soup)
        self.__save("1")

    def __save(self, name: str):
        csv_file = open("./data/" + FILENAME + ".csv", "a")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(self.processed_soup)

    def __process(self, raw):
        pass

    def __str__(self):
        resp = requests.get(self.url)
        soup = bs(resp.text, "lxml")
        return soup


pars = SiteParser(site_urls[0])  # one element for testing
pars.run()
