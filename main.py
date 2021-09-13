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
        "Размер": "",
        "Открывание": "",
        "Тип товаров": "",
        "Остекление": "",
    }
    __first_iter = True

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
        self._csv_filename = "./data/" + FILENAME + "3.csv"
        self.__create_columns()
        self.print_r("Load configs...")
        self.__current_iteration: int = 0
        self.product: dict
        self.__sku_code: int

    def run(self, url: list) -> None:
        """ Запуск """
        self.product: dict = {
            "name": '',
            "img": '',
            "color": '',
            "material": '',
            "height": '',
            "width": '',
            "depth": '',
            "sku": '',
            "price": '',
            'size': '',
            'opening': '',
            'description': '',
            'glass': '',
        }
        if url != "":
            self.url = url
        self.driver.get(self.url[0])
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        PRODUCT_TYPE = self.url[1]
        self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')
        self.save_columns['Наименование'] = self.product['name']
        self.save_columns['ID артикула'] = self.__sku_code
        self.save_columns['Код артикула'] = self.product['sku']
        self.save_columns['Наименование артикула'] = self.product['sku']
        self.save_columns['Цена'] = self.product['price']
        self.save_columns['Изображения товаров'] = self.product['img']
        self.save_columns['Описание'] = self.product['description']
        self.save_columns['Тип товаров'] = PRODUCT_TYPE
        self.save_columns['Открывание'] = self.product["opening"]
        self.save_columns['Размер'] = self.product['size']
        self.save_columns['Открывание'] = self.product['opening']
        self.save_columns['Цвет'] = self.product['color']
        self.save_columns['Материал'] = self.product['material']
        self.save_columns['Остекление'] = self.product['glass']

        # Запись в файл
        with open(self._csv_filename, "a", encoding='utf8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns.values())

    def __create_columns(self) -> None:
        """ Создание файла CSV """
        self.print_r(f"First init CSV file: {self._csv_filename}...")
        with open(self._csv_filename, "w", encoding='utf8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns)

    def __process(self) -> None:
        """ Обработчик """
        try:
            self.__get_next_product()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_next_product(self) -> None:
        """ Переключение продукта """
        self.print_r("Getting next product...")
        self.__sku_code = 0
        try:
            __parent = self.driver.find_elements_by_css_selector(
                "div.razdel-wrap div.latest-item")
            for __child in __parent:
                self.__product = __child
                self.__get_data()
                self.__sku_code += 1
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            self.__first_iter = False
            self.__get_product_name()
            self.__get_product_price()
            self.__get_product_img()
            # self.__get_product_description()
            self.__get_product_sku()
            self.__save()
            self.print_r(
                f"Product {self.product['name']} added for {self.float_to_fixed(float(time() - self.ttimer), 2)} sec")
        except Exception as error:
            self.print_r(f"{error}", "e")
        return self.product

    def __get_product_name(self) -> None:
        """ Получение наименование товара """
        self.print_r("Getting product name...")
        try:
            __name = self.__product.find_element_by_css_selector("h4").text
            self.product['name'] = __name.capitalize()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_sku(self) -> None:
        """ Получение артикула товара """
        self.print_r("Getting product sku...")
        try:
            self.product['sku'] = f"ДВ-{self.product['name'].split(' ')[1][:3]}-{self.__sku_code}".upper()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_price(self) -> None:
        """ Получение цены товара """
        self.print_r("Getting product price...")
        try:
            self.product['price'] = self.__product.find_element_by_css_selector("div.latest-price").text.split("от ")[1].split(" руб")[0]
        except Exception as error:
            self.product['price'] = "0"
            self.print_r(f"{error}", "e")

    def __get_product_description(self) -> None:
        """ Получение описания товара """
        self.print_r("Getting product description...")
        try:
            __parent = self.driver.find_element_by_css_selector(
                'div.tabs__content.active.clearfix div.option p').text.split("<br>")
            __desc: list = []
            for __child in __parent:
                if 'Материал' in __child:
                    self.product['material'] = __child.split(": ")[2].split("\n")[0]
                __desc.append(__child.strip())
            self.product['description'] = '. '.join(__desc)
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_img(self) -> None:
        """ Получение изображений товара """
        self.print_r("Getting product image...")
        try:
            self.product['img'] = self.__product.find_element_by_css_selector(
                'div.latest-img img').get_attribute('src')
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __close_jivo(self) -> None:
        """ Закрытие бизнес-мессенджера Jivo """
        self.driver.execute_script('''$("div.jivo-iframe-container").remove();''')
        self.driver.execute_script('''$("jdiv").remove();''')
        sleep(0.5)

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
