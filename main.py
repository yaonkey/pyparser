#!/usr/bin/env python3
import time
import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep, time, strftime, ctime
from config import *
import sys


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
    }
    save_columns: dict = {
        "Тип строки": "product_variant",
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
        "Ширина": ""
    }

    def __init__(self, url: str == "") -> None:
        self.__timer = time()
        self.print_r('Init timer')
        if url != "":
            self.url = url
        options = Options()
        options.headless = IS_BROWSER_HIDE
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')
        self._csv_filename = "./data/" + FILENAME + ".csv"
        self.__create_columns()
        self.print_r("Load configs...")

    def run(self, url: str = "") -> None:
        """ Запуск """
        if url != "":
            self.url = url
        self.driver.get(self.url)
        sleep(7)
        self.__get_root_home_page()
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        if DEBUG:
            self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')

        self.sku_code += 1
        self.save_columns['Наименование'] = self.product['name']
        self.save_columns['Код артикула'] = self.sku_code
        self.save_columns['Наименование артикула'] = self.product['sku']
        self.save_columns['Цена'] = self.product['price']
        self.save_columns['Изображения товаров'] = self.product['img']
        self.save_columns['Цвет'] = self.product['color']
        self.save_columns['Материал'] = self.product['material']
        self.save_columns['Высота'] = self.product['height']
        self.save_columns['Толщина'] = self.product['depth']
        self.save_columns['Ширина'] = self.product['width']

        with open(self._csv_filename, "a", encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns.values())

    def __create_columns(self) -> None:
        """ Создание файла CSV """
        self.print_r(f"First init CSV file: {self._csv_filename}...")
        with open(self._csv_filename, "w", encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns)

    def __process(self) -> None:
        """ Обработчик """
        try:
            self.__get_next_material_by_click()
        except Exception as error:
            self.print_r(f"{error}")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            sleep(1)
            product_div = self.__get_root_home_page()
            self.product["name"] = " ".join(f"{product_div.find('h2').get_text()}".split(" ")[0:2])
            self.print_r(f"Get product {self.product['name']} additional values...")
            self.product[
                'img'] = f"https://{FILENAME}.ru{product_div.find('a', {'data-fancybox': 'shop-item-photo'}).find('img')['src']}"
            self.product["sku"] = product_div.find_all("span", {"class": "text-danger"})[0].get_text().split(" ")[1]
            self.product["price"] = ''.join(
                [elem for elem in product_div.find_all("span", {"class": "text-danger"})[1].get_text().split(" ")[1] if
                 elem != '\xa0'])
            self.__close_jivo()
            self.__save()
            self.print_r(f"Product {self.product['name']} added for {self.float_to_fixed(float(time() - self.ttimer), 2)} sec")
            sleep(0.4)
        except Exception as error:
            self.print_r(f"{error}")
        return self.product

    def __get_next_material_by_click(self) -> None:
        """ Переключение материала продукта """
        self.print_r("Getting next material...")
        try:
            material_buttons_ids = self.driver.find_elements_by_css_selector("input[type=radio].custom-control-input")
            for element_button in material_buttons_ids:
                if 'colorType' in element_button.get_attribute('id'):
                    __button = self.driver.find_element_by_css_selector(
                        f'''label[for='{element_button.get_attribute("id")}']''')
                    self.product['material'] = __button.text
                    __button.click()
                    sleep(3.5)
                    self.__close_jivo()
                    self.__get_next_color_by_click()
                else:
                    continue
        except Exception as error:
            self.print_r(f"{error}")

    def __get_next_color_by_click(self) -> None:
        """ Переключение цвета продукта """
        self.print_r("Getting next color...")
        try:
            color_buttons_ids = self.driver.find_elements_by_css_selector(
                "input[type='radio'].custom-control-input")
            for element_button in color_buttons_ids:
                if 'colorType' not in element_button.get_attribute('id') and 'color' in element_button.get_attribute(
                        'id'):
                    __button = self.driver.find_element_by_css_selector(
                        f'''label[for='{element_button.get_attribute("id")}']''')
                    self.product['color'] = __button.text
                    __button.click()
                    sleep(3.5)
                    self.__close_jivo()
                    self.__get_next_height_by_click()
                else:
                    continue
        except Exception as error:
            self.print_r(f"{error}")

    def __get_next_height_by_click(self) -> None:
        """ Переключение высоты продукта """
        self.print_r("Getting next height value...")
        try:
            height_buttons_ids = self.driver.find_elements_by_css_selector(
                "select#property_height option")
            for element_button in height_buttons_ids:
                __button = element_button
                self.product['height'] = __button.text
                __button.click()
                sleep(3.5)
                self.__close_jivo()
                self.__get_next_width_by_click()
        except Exception as error:
            self.print_r(f"{error}")

    def __get_next_width_by_click(self) -> None:
        """ Переключение ширины продукта """
        self.print_r("Getting next width value...")
        try:
            width_buttons_ids = self.driver.find_elements_by_css_selector(
                "select#property_width option")
            for element_button in width_buttons_ids:
                __button = element_button
                self.product['width'] = __button.text
                __button.click()
                sleep(3.5)
                self.__close_jivo()
                self.__get_next_depth_by_click()
        except Exception as error:
            self.print_r(f"{error}")

    def __get_next_depth_by_click(self) -> None:
        """ Переключение толщины продукта """
        self.print_r("Getting next depth value...")
        try:
            depth_buttons_ids = self.driver.find_elements_by_css_selector(
                "select#property_wall_thickness option")
            for element_button in depth_buttons_ids:
                __button = element_button
                self.product['depth'] = __button.text
                __button.click()
                sleep(3.5)
                self.__close_jivo()
                self.__get_data()
        except Exception as error:
            self.print_r(f"{error}")

    def __close_jivo(self) -> None:
        """ Закрытие бизнес-мессенджера Jivo """
        self.driver.execute_script('''$("div.jivo-iframe-container").remove();''')
        self.driver.execute_script('''$("jdiv").remove();''')
        sleep(0.5)

    def __get_root_home_page(self) -> any:
        """ Получение HTML-страницы текущего url """
        self.html = self.driver.page_source
        self.soup = bs(self.html, "lxml")
        self.root_home_page = self.soup.find('div', {"class", "home"})
        sleep(1)
        return self.root_home_page

    def print_r(self, text: str) -> None:
        """ Кастомный print и logger в одном методе """
        sys.stdout.write(f"\r[{ctime(self.__timer)}]: {text}")
        sys.stdout.flush()
        with open('./logs/work.log', 'a+', encoding='utf-8') as log_file:
            log_file.write(f"\n[{strftime('%Y.%b.%d %X')} | {self.float_to_fixed(time() - self.__timer, 3)}s]: {text}")

    def float_to_fixed(self, num_obj, digits=0) -> str:
        """ Для работы с double """
        return f"{num_obj:.{digits}f}"

    def __del__(self) -> None:
        """ Закрытие драйвера браузера при удалении """
        self.print_r(f"Program close at {int(time() - self.__timer)} sec")
        self.driver.quit()


mode = 1
pars = SiteParser(url="")
if mode == 1:
    for url in SITE_URLS:
        pars.run(url)
elif mode == 0:
    pars.run(SITE_URLS[0])
