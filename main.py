#!/usr/bin/env python3
import time
from re import sub
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
        "Материал": "",
        "Тип товаров": PRODUCT_TYPE,
        "Характеристики": "",
    }
    __first_iter = True
    __sku_code = 0

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
        self.__current_iteration: int = 0
        self.product: dict

    def run(self, url: list) -> None:
        """ Запуск """
        if self.__current_iteration <= MAX_PRODUCTS_ON_ONE_PAGE:
            self.__current_iteration += 1
        else:
            self.__current_iteration = 1
        self.product: dict = {
            "name": '',
            "img": "",
            "color": '',
            "material": '',
            "sku": '',
            "price": '',
            'description': '',
            'specs': ''
        }
        if url != "":
            self.url = url
        self.driver.get(self.url)
        self.__sku_code += 1
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        self.__sku_code += 1
        self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')
        self.save_columns['Наименование'] = self.product['name']
        self.save_columns['ID артикула'] = self.__sku_code
        self.save_columns[
            'Код артикула'] = f"{PRODUCT_TYPE[0]}-{self.product['name'][4]}-{self.__sku_code}-{self.product['sku']}".upper()
        self.save_columns['Наименование артикула'] = self.product['sku']
        self.save_columns['Цена'] = self.product['price']
        self.save_columns['Изображения товаров'] = self.product['img']
        self.save_columns['Описание'] = self.product['description']
        self.save_columns['Материал'] = self.product['material']
        self.save_columns['Характеристики'] = self.product['specs']

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
            sleep(3)
            self.__get_data()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            self.__first_iter = False
            self.__get_product_name()
            self.__get_product_sku()
            self.__get_product_material()
            self.__get_product_price()
            self.__get_product_description()
            self.__get_product_img()
            self.__get_product_specs()
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
            __name = self.driver.find_element_by_css_selector("div.maincol__i h1").text
            __name = sub(r'\([^()]*\)', '', __name)
            self.product['name'] = __name.strip()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_sku(self) -> None:
        """ Получение артикула товара """
        self.print_r("Getting product sku...")
        try:
            self.product['sku'] = \
                self.driver.find_element_by_css_selector('div.maincol__i span.product-id').text.split(": ")[1].strip()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_material(self) -> None:
        """ Получение материала продукта """
        self.print_r("Getting product material...")
        try:
            self.product['material'] = \
                self.driver.find_element_by_css_selector("div.maincol__i h1").text.split('(')[-1].split(")")[0].capitalize()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_price(self) -> None:
        """ Получение цены товара """
        self.print_r("Getting product price...")
        try:
            self.product['price'] = self.driver.find_element_by_css_selector(
                "div.card__priceval span.price.rub").text.strip()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_description(self) -> None:
        """ Получение описания товара """
        self.print_r("Getting product description...")
        try:
            self.product['description'] = self.driver.find_element_by_css_selector('div#description').text.strip()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_img(self) -> None:
        """ Получение изображений товара """
        self.print_r("Getting product image...")
        try:
            __imgs = self.driver.find_elements_by_css_selector('img.fotorama__img')
            __img_list = [img.get_attribute('src') for img in __imgs]
            self.product['img'] = ', '.join(set(__img_list))
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_specs(self) -> None:
        """ Получение характеристик продукта """
        try:
            __parent = self.driver.find_elements_by_css_selector(
                "div.shift_element.aligned-row div.char-item.limited.item_element.item")
            __temp_child = []
            for __first_child in __parent:
                __second_child = __first_child.find_elements_by_css_selector("table.char.table_1.table tbody tr")
                for __third_child in __second_child:
                    __first_element = __third_child.find_element_by_css_selector("th").get_attribute('innerHTML')
                    __second_element = __third_child.find_element_by_css_selector("td").get_attribute('innerHTML')
                    __temp_child.append(f"{__first_element}: {__second_element};")
            self.product['specs'] = ' '.join(__temp_child)
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
