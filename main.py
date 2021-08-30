#!/usr/bin/env python3
import time

import requests
from bs4 import BeautifulSoup as bs
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from time import sleep, time
from config import *


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
    max_iteration_on_one_material: int
    __iter: int = 0
    first_iter: bool = True

    def __init__(self, url: str == ""):
        self.__timer = time()
        if url != "":
            self.url = url
        options = Options()
        options.headless = IS_BROWSER_HIDE
        self.driver = webdriver.Firefox(options=options, executable_path=rf'{SELENIUM_PATH}')

    def run(self, url: str = ""):
        if url != "":
            self.url = url
        self.driver.get(self.url)
        sleep(7)
        self.__get_root_home_page()
        self.__process()
        self.__save()

    def __save(self):
        if DEBUG:
            print(self.product)
        with open("./data/" + FILENAME + ".csv", "a") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(self.product)

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

        self.max_iteration_on_one_material = len(self.product["color"]) * len(self.product["height"]) * len(
            self.product["width"]) * len(self.product["depth"])
        self.driver.execute_script('''$("div.jivo-iframe-container").remove();''')
        if self.first_iter:
            self.__get_next_material_by_click()
        return self.product

    def __get_page_from_url(self):
        return bs(requests.get(self.url).text, "lxml")

    def __get_next_material_by_click(self):
        self.__get_root_home_page()
        material_buttons_ids = [material['id'] for material in
                                self.root_home_page.find_all("input",
                                                             {"type": "radio", "class": "custom-control-input"}) if
                                'colorType' in material['id']]
        self.first_iter = False
        for element_button in material_buttons_ids:
            __button = self.driver.find_element_by_css_selector(f"label[for='{element_button}']")
            self.product['material'] = __button.text
            __button.click()
            sleep(7)
            self.__close_jivo()
            self.__get_next_color_by_click()

    def __get_next_color_by_click(self):
        self.__get_root_home_page()
        color_buttons_ids = [color['id'] for color in
                             self.root_home_page.find_all("input",
                                                          {"type": "radio", "class": "custom-control-input"}) if
                             'colorType' not in color['id'] and 'color' in color['id']]
        for element_button in color_buttons_ids:
            __button = self.driver.find_element_by_css_selector(f"label[for='{element_button}']")
            self.product['color'] = __button.text
            __button.click()
            sleep(7)
            self.__close_jivo()
            self.__get_next_height_by_click()

# todo: fix bug with empty height selector
    def __get_next_height_by_click(self):
        self.__get_root_home_page()
        height_select_button = self.root_home_page.find("select", {"id": "property_height"})
        height_buttons_ids = height_select_button.find_all('option')
        for element_button in height_buttons_ids:
            __button = self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['height'] = __button.text
            __button.click()
            sleep(7)
            self.__close_jivo()
            self.__get_next_width_by_click()

    def __get_next_width_by_click(self):
        self.__get_root_home_page()
        width_select_button = self.root_home_page.find("select", {"id": "property_width"})
        width_buttons_ids = width_select_button.find_all('option')
        for element_button in width_buttons_ids:
            __button = self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['width'] = __button.text
            __button.click()
            sleep(7)
            self.__close_jivo()
            self.__get_next_depth_by_click()

    def __get_next_depth_by_click(self):
        self.__get_root_home_page()
        depth_select_button = self.root_home_page.find("select", {"id": "property_wall_thickness"})
        depth_buttons_ids = depth_select_button.find_all('option')
        for element_button in depth_buttons_ids:
            __button = self.driver.find_element_by_css_selector(f"""option[value='{element_button["value"]}']""")
            self.product['depth'] = __button.text
            __button.click()
            sleep(7)
            self.__close_jivo()
            self.__process()

    def __close_jivo(self):
        self.driver.execute_script('''$("div.jivo-iframe-container").remove();''')
        self.driver.execute_script('''$("jdiv").remove();''')
        sleep(2)

    def __get_root_home_page(self):
        self.html = self.driver.page_source
        self.soup = bs(self.html, "lxml")
        self.root_home_page = self.soup.find('div', {"class", "home"})
        sleep(1)
        return self.root_home_page

    def __del__(self):
        print(f"{int(time() - self.__timer)} sec")
        self.driver.quit()


delo = 0
pars = SiteParser(url="")
if delo == 1:
    for url in SITE_URLS:
        pars.run(url)
elif delo == 0:
    pars.run(SITE_URLS[0])
