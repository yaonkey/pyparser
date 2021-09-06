#!/usr/bin/env python3
import time
import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep, time, strftime, gmtime
from config import *
import sys
import logging


class SiteParser:
    product: dict = {
        "name": '',
        "img": '',
        "color": '',
        "material": '',
        "height": '',
        "width": '',
        "depth": '',
        "sku": '',
        "price": '',
        'size': ''
    }
    save_columns: dict = {
        "Наименование": "",
        "Наименование артикула": "",
        "Код артикула": "",
        "Валюта": "RUB",
        "ID артикула": "",
        "Цена": "",
        "Доступен для заказа": "1",
        "Зачеркнутая цена": "0",
        "Закупочная цена": "0",
        "В наличии": "1000",
        "ID товара": "",
        "Краткое описание": "",
        "Описание": "",
        "Наклейка": "",
        "Статус": "",
        "Выбор вариантов товара": "",
        "Тип товаров": "",
        "Теги": "",
        "Облагается налогом": "",
        "Заголовок": "",
        "META Keywords": "",
        "META Description": "",
        "Ссылка на витрину": "",
        "Адрес видео на YouTube или Vimeo": "",
        "Дополнительные параметры": "",
        "Изображения товаров": "",
        "Цвет": "",
        "Материал": "",
        "Высота": "",
        "Толщина": "",
        "Ширина": "",
        "Размер": ""
    }

    def __init__(self) -> None:
        self.__timer = time()
        logging.basicConfig(filename=LOG_PATH + "debug.log", filemode='a', level=logging.ERROR, encoding='utf-8',
                            format='[%(asctime)s]: %(levelname)s | %(name)s | %(message)s', datefmt='%Y.%b.%d %H:%M:%S')
        self.print_r('Init timer')
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.headless = IS_BROWSER_HIDE
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')
        self._csv_filename = "./data/" + FILENAME + ".csv"
        self.__create_columns()
        self.print_r("Load configs...")

    def run(self, url: list) -> None:
        """ Запуск """
        if url != "":
            self.url = url
        self.driver.get(self.url[0])
        PRODUCT_TYPE = self.url[1]
        self.product['sku_code'] = 0
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')
        self.product['ID'] += 1
        self.product['sku_code'] += 1
        self.save_columns['ID'] = self.product['ID']
        self.save_columns['Name'] = self.product['name']
        self.save_columns['Article number'] = self.product['sku_code']
        self.save_columns['Article name'] = self.product['sku']
        self.save_columns['Price'] = self.product['price']
        self.save_columns['Underlined price'] = self.product['underlined price']
        self.save_columns['Image'] = self.product['img']
        self.save_columns['Description'] = self.product['description']
        self.save_columns['Product type'] = self.url[1]

        with open(self._csv_filename, "a", encoding='utf8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns.values())

        self.__get_next_product_by_click()

    def __create_columns(self) -> None:
        """ Создание файла CSV """
        self.print_r(f"First init CSV file: {self._csv_filename}...")
        with open(self._csv_filename, "w", encoding='utf8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns)

    def __process(self) -> None:
        """ Обработчик """
        try:
            self.__get_next_product_by_click()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            sleep(3)
            self.__get_product_name()
            self.__get_product_price()
            self.__get_underlined_price()
            self.__get_product_img()
            self.__get_product_description()
            self.__get_product_sku()
            self.__save()
            self.print_r(
                f"Product {self.product['name']} added for {self.float_to_fixed(float(time() - self.ttimer), 2)} sec")
        except Exception as error:
            self.print_r(f"{error}", "e")
        return self.product

    def __get_next_product_by_click(self) -> None:
        """ Переключение продукта """
        self.print_r("Getting next product...")
        try:
            sleep(7)
            product_button = self.driver.find_element_by_css_selector(
                "div#wk_right_nav")
            self.__get_data()
            product_button.click()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_name(self) -> None:
        """ Получение наименование товара """
        self.print_r("Getting product name...")
        try:
            self.product['name'] = self.driver.find_element_by_css_selector("div.market_item_title").text
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_sku(self) -> None:
        """ Получение артикула товара """
        self.print_r("Getting product sku...")
        try:
            self.product['sku'] = f'''{self.url[1][:2]}-{self.product["sku_code"]}'''
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_price(self) -> None:
        """ Получение цены товара """
        self.print_r("Getting product price...")
        try:
            __price = self.driver.find_element_by_css_selector("span.market-item-price").text.split(" ")[0]
            if "," in __price:
                __price = __price.replace(",", "")
            self.product['price'] = __price
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_description(self) -> None:
        self.print_r("Getting product description...")
        try:
            self.product['description'] = self.driver.find_element_by_css_selector('div#market_item_description').text
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_underlined_price(self) -> None:
        self.print_r("Getting underlined price...")
        try:
            self.product['underlined price'] = int(self.product['price']) + 150
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_img(self) -> None:
        """ Получение изображений товара """
        self.print_r("Getting product image...")
        try:
            __parent = self.driver.find_elements_by_css_selector("div.ui_scroll_content div")
            for __child in __parent:
                __img = self.driver.find_element_by_css_selector("img#market_item_photo")
                __img.click()
                sleep(1)
                self.product['img'].append(__img.get_attribute("src"))
        except Exception as error:
            self.print_r(f"{error}", "e")
            self.product['img'].append('')

    def print_r(self, text: str, print_type: str = "i") -> None:
        """ Кастомный print и logger в одном методе """
        sys.stdout.write(f"\r[{strftime('%H:%M:%S', gmtime(time() - self.__timer))}]: {text}")
        sys.stdout.flush()
        if print_type == "i":
            logging.info(text)
        elif print_type == 'w':
            logging.warning(text)
        elif print_type == 'e':
            logging.error(text)
        elif print_type == 'ex':
            logging.exception(text)

    def float_to_fixed(self, num_obj, digits=0) -> str:
        """ Для работы с double """
        return f"{num_obj:.{digits}f}"

    def __del__(self) -> None:
        """ Закрытие драйвера браузера при удалении """
        self.print_r(f"Program close at {int(time() - self.__timer)} sec")
        self.driver.quit()


pars = SiteParser()
for url in SITE_URLS:
    pars.run(url)
