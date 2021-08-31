#!/usr/bin/env python3
import time
import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep, time
from config import *
import sys
from random import choice


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
    }
    save_columns = {
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

    def __init__(self, url: str == ""):
        self.print_r('Init timer')
        self.__timer = time()
        if url != "":
            self.url = url
        options = Options()
        options.headless = IS_BROWSER_HIDE
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')
        self.first_iter: bool = True
        self._csv_filename = "./data/" + FILENAME + ".csv"
        self.print_r("Load configs...")

    def run(self, url: str = ""):
        if url != "":
            self.url = url
        self.driver.get(self.url)
        sleep(7)
        self.__get_root_home_page()
        self.__process()

    def __save(self):
        if DEBUG:
            self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')
            self.save_columns = {
                "Тип строки": "product_variant",
                "Наименование": self.product["name"],
                "Наименование артикула": self.product["sku"],
                "Код артикула": "",
                "Валюта": "RUB",
                "ID артикула": "",
                "Цена": self.product["price"],
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
                "Изображения товаров": self.product["img"],
                "Цвет": self.product["color"],
                "Материал": self.product["material"],
                "Высота": self.product["height"],
                "Толщина": self.product["depth"],
                "Ширина": self.product["width"]
            }

        with open(self._csv_filename, "a", encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns.values())

    def __create_columns(self):
        self.print_r(f"First init CSV file: {self._csv_filename}...")
        self.first_iter = False
        with open(self._csv_filename, "w", encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow(self.save_columns)

    def __process(self):
        product_div = self.__get_root_home_page()
        self.product["name"] = " ".join(f"{product_div.find('h2').get_text()}".split(" ")[0:2])
        self.product[
            'img'] = f"https://{FILENAME}.ru{product_div.find('a', {'data-fancybox': 'shop-item-photo'}).find('img')['src']}"
        # self.product['material'] = [material.text.strip() for material in product_div.find_all('label', {
        #     'for': [mid['id'] for mid in
        #             product_div.find_all("input", {"type": "radio", "class": "custom-control-input"}) if
        #             'colorType' in mid['id']]})]
        # self.product["color"] = [color.text.strip() for color in product_div.find_all('label', {
        #     'for': [mid['id'] for mid in
        #             product_div.find_all("input", {"type": "radio", "class": "custom-control-input"}) if
        #             'color' in mid['id'] and 'colorType' not in mid['id']]})]
        # self.product["height"] = [height.text.strip() for height in
        #                           product_div.find("select", {"id": "property_height"}).find_all("option")]
        # self.product["width"] = [width.text.strip() for width in
        #                          product_div.find("select", {"id": "property_width"}).find_all("option")]
        # self.product["depth"] = [depth.text.strip() for depth in
        #                          product_div.find("select", {"id": "property_wall_thickness"}).find_all("option")]
        self.product["sku"] = product_div.find_all("span", {"class": "text-danger"})[0].get_text().split(" ")[1]
        self.product["price"] = ''.join(
            [elem for elem in product_div.find_all("span", {"class": "text-danger"})[1].get_text().split(" ")[1] if
             elem != '\xa0'])

        self.__close_jivo()
        if self.first_iter:
            self.__create_columns()
            self.__get_next_material_by_click()
        self.__save()
        return self.product

    def __get_page_from_url(self):
        return bs(requests.get(self.url).text, "lxml")

    def __get_next_material_by_click(self):
        self.print_r("Getting next material...")
        self.__get_root_home_page()
        material_buttons_ids = self.driver.find_elements_by_css_selector("input[type=radio].custom-control-input")
        # [material['id'] for material in
        #                     self.root_home_page.find_all("input",
        #                                                  {"type": "radio", "class": "custom-control-input"}) if
        #                     'colorType' in material['id']]
        for element_button in material_buttons_ids[0:2]:
            if 'colorType' in element_button.get_attribute('id'):
                __button = self.driver.find_element_by_css_selector(
                    f'''label[for='{element_button.get_attribute("id")}']''')
                self.product['material'] = __button.text
                __button.click()
                sleep(3)
                self.__close_jivo()
                self.__get_next_color_by_click()
            else:
                continue

    def __get_next_color_by_click(self):
        self.print_r("Getting next color...")
        self.__get_root_home_page()
        color_buttons_ids = self.driver.find_elements_by_css_selector(
            "input[type='radio'].custom-control-input")  # [color['id'] for color in
        # self.root_home_page.find_all("input",
        #                              {"type": "radio", "class": "custom-control-input"}) if
        # 'colorType' not in color['id'] and 'color' in color['id']]
        for element_button in color_buttons_ids:
            if 'colorType' not in element_button.get_attribute('id') and 'color' in element_button.get_attribute('id'):
                __button = self.driver.find_element_by_css_selector(
                    f'''label[for='{element_button.get_attribute("id")}']''')
                self.product['color'] = __button.text
                __button.click()
                sleep(3)
                self.__close_jivo()
                self.__get_next_height_by_click()
            else:
                continue

    def __get_next_height_by_click(self):
        self.print_r("Getting next height value...")
        self.__get_root_home_page()
        # height_select_button = self.root_home_page.find("select", {"id": "property_height"})
        height_buttons_ids = self.driver.find_elements_by_css_selector(
            "select#property_height option")  # height_select_button.find_all('option')
        for element_button in height_buttons_ids:
            __button = element_button  # self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['height'] = __button.text
            __button.click()
            sleep(3)
            self.__close_jivo()
            self.__get_next_width_by_click()

    def __get_next_width_by_click(self):
        self.print_r("Getting next width value...")
        self.__get_root_home_page()
        # width_select_button = self.root_home_page.find("select", {"id": "property_width"})
        width_buttons_ids = self.driver.find_elements_by_css_selector(
            "select#property_width option")  # width_select_button.find_all('option')
        for element_button in width_buttons_ids:
            __button = element_button  # self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['width'] = __button.text
            __button.click()
            sleep(3)
            self.__close_jivo()
            self.__get_next_depth_by_click()

    def __get_next_depth_by_click(self):
        self.print_r("Getting next depth value...")
        self.__get_root_home_page()
        # depth_select_button = self.root_home_page.find("select", {"id": "property_wall_thickness"})
        depth_buttons_ids = self.driver.find_elements_by_css_selector(
            "select#property_wall_thickness option")  # depth_select_button.find_all('option')
        for element_button in depth_buttons_ids:
            __button = element_button  # self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['depth'] = __button.text
            __button.click()
            sleep(3)
            self.__close_jivo()
            self.__process()

    def __close_jivo(self):
        # self.print_r("Closing Jivo...")
        self.driver.execute_script('''$("div.jivo-iframe-container").remove();''')
        self.driver.execute_script('''$("jdiv").remove();''')
        sleep(0.5)

    def __get_root_home_page(self):
        # self.print_r("Getting root page...")
        self.html = self.driver.page_source
        self.soup = bs(self.html, "lxml")
        self.root_home_page = self.soup.find('div', {"class", "home"})
        sleep(1)
        return self.root_home_page

    def print_r(self, text) -> None:
        symb = choice(["-x", "--", "x-", "xx"])
        sys.stdout.write(f"\r[{symb}] {text}")
        sys.stdout.flush()

    def __del__(self):
        self.print_r(f"Program close at {int(time() - self.__timer)} sec")
        self.driver.quit()


delo = 0
pars = SiteParser(url="")
if delo == 1:
    for url in SITE_URLS:
        pars.run(url)
elif delo == 0:
    pars.run(SITE_URLS[0])
