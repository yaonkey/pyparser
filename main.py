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
    sku_code: int = 0
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
        'size': '',
        'opening': '',
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
        "Тип товаров": "Дверь",
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
    }

    def __init__(self) -> None:
        self.__timer = time()
        logging.basicConfig(filename=LOG_PATH + "debug.log", filemode='a', level=logging.ERROR, encoding='utf-8',
                            format='[%(asctime)s]: %(levelname)s | %(name)s | %(message)s', datefmt='%Y.%b.%d %H:%M:%S')
        self.print_r('Init timer')
        options = Options()
        options.headless = IS_BROWSER_HIDE
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')
        self._csv_filename = "./data/" + FILENAME + ".csv"
        self.__create_columns()
        self.print_r("Load configs...")

    def run(self, url: list) -> None:
        """ Запуск """
        if url != "":
            self.url = url
        self.driver.get(self.url)
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')

        self.sku_code += 1
        self.save_columns['Наименование'] = self.product['name']
        self.save_columns['Код артикула'] = self.sku_code
        self.save_columns['Наименование артикула'] = self.product['sku']
        self.save_columns['Цена'] = self.product['price']
        self.save_columns['Изображения товаров'] = self.product['img']
        self.save_columns['Цвет'] = self.product['color']
        self.save_columns['Материал'] = self.product['material']
        self.save_columns["Размер"] = self.product['size']
        self.save_columns['Высота'] = self.product['height']
        self.save_columns['Толщина'] = self.product['depth']
        self.save_columns['Ширина'] = self.product['width']
        self.save_columns['Открывание'] = self.product['opening']

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
            self.__get_next_size_by_click()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            sleep(3)
            self.__get_product_name()
            self.__get_product_price()
            self.__get_product_img()
            self.__get_product_color()
            self.__get_product_material()
            self.__get_product_sku()
            self.__save()
            self.print_r(
                f"Product {self.product['name']} added for {self.float_to_fixed(float(time() - self.ttimer), 2)} sec")
        except Exception as error:
            self.print_r(f"{error}", "e")
        return self.product

    def __get_next_size_by_click(self) -> None:
        """ Переключение размера продукта """
        self.print_r("Getting next size...")
        try:
            size_buttons = self.driver.find_elements_by_css_selector(
                "ul.list_values_wrapper li")
            for element_button in size_buttons:
                if 'Размер' in element_button.get_attribute('title'):
                    self.product['size'] = element_button.find_element_by_css_selector("span").text.split(" ")[0]
                    element_button.click()
                    self.__get_next_opening_by_click()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_next_opening_by_click(self) -> None:
        """ Переключение кнопки способа открывания """
        self.print_r("Getting next opening side...")
        try:
            opening_buttons = self.driver.find_elements_by_css_selector(
                "ul.list_values_wrapper li")
            for element_button in opening_buttons:
                if 'Открывание' in element_button.get_attribute('title'):
                    self.product['opening'] = element_button.find_element_by_css_selector("span").text
                    element_button.click()
                    self.__get_data()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_name(self) -> None:
        """ Получение наименование товара """
        self.print_r("Getting product name...")
        try:
            self.product['name'] = " ".join(
                self.driver.find_element_by_css_selector("h1#pagetitle").text.split(" ")[:3])
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_sku(self) -> None:
        """ Получение артикула товара """
        self.print_r("Getting product sku...")
        try:
            self.product[
                'sku'] = f'''ВД-{''.join([c[:2] for c in self.product['name'].split(" ")[2]][:3])}-{self.product["size"].split("х")[0]}{self.product["opening"][0]}'''
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_price(self) -> None:
        """ Получение цены товара """
        self.print_r("Getting product price...")
        try:
            self.product['price'] = ''.join(self.driver.find_element_by_css_selector("span.price_value").text.split(" "))
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_img(self) -> None:
        """ Получение изображения товара """
        self.print_r("Getting product image...")
        try:
            self.product['img'] = self.driver.find_element_by_css_selector(
                "a.popup_link.fancy_offer").get_attribute('href')
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_color(self) -> None:
        """ Получение цвета товара """
        self.print_r("Getting product color...")
        try:
            __parent = self.driver.find_elements_by_css_selector('div.detail_text div.row p.col-md-4')
            self.product['color'] = __parent[-1].text.split(":")[1].split(";")[0].strip()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_material(self) -> None:
        """ Получение материала товара """
        self.print_r("Getting product material...")
        try:
            self.product['material'] = 'МДФ'
        except Exception as error:
            self.print_r(f"{error}", "e")

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
