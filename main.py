#!/usr/bin/env python3
import time
import csv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    __sku_code = 0

    def __init__(self) -> None:
        self.current_product = ''
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
        self.__sizes = ['550х1900', '600х1900', '600х2000', '700х2000', '800х2000', '900х2000']
        if url != "":
            self.url = url
        self.driver.get(self.url[0])
        self.__sku_code += 1
        self.__process()

    def __save(self) -> None:
        """ Сохранение в CSV """
        self.__sku_code += 1
        self.print_r(f'Saving product sku: {self.product["sku"]} to {self._csv_filename}...')
        self.save_columns['Наименование'] = self.product['name']
        self.save_columns['ID артикула'] = self.__sku_code
        self.save_columns['Код артикула'] = f"{self.product['sku']}"
        self.save_columns['Наименование артикула'] = self.product['sku']
        self.save_columns['Цена'] = self.product['price']
        self.save_columns['Изображения товаров'] = self.product['img']
        self.save_columns['Описание'] = self.product['description']
        self.save_columns['Тип товаров'] = self.url[1]
        self.save_columns['Открывание'] = self.product["opening"]
        self.save_columns['Открывание'] = self.product['opening']
        self.save_columns['Цвет'] = self.product['color']
        self.save_columns['Материал'] = self.product['material']
        self.save_columns['Остекление'] = self.product['glass']

        for _size in self.__sizes:
            self.save_columns['Размер'] = _size
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
            self.__get_next_product_by_click()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_next_product_by_click(self) -> None:
        """ Переключение продукта """
        self.print_r("Getting next product...")
        try:
            sleep(3)
            self.__close_jivo()
            __parent = WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div.catalog.horizont ul li.catalog_item")))
            for __product in __parent:
                self.driver.execute_script("arguments[0].scrollIntoView()", __product)
                # ActionChains(self.driver).move_to_element(__product).perform()  # animation
                self.current_product = __product
                self.__get_product_name()
                self.__get_product_price()
                self.__get_product_img()
                self.__get_product_glass_and_color()
                self.__get_product_sku()
                self.__save()
            else:
                self.print_r("Products is end on this page!", "e")
        except TimeoutException:
            self.print_r(f"Timeout on getting next product", "e")

    def __get_data(self) -> dict:
        """ Получение данных о товаре """
        try:
            self.ttimer = time()
            self.__first_iter = False
            self.__get_product_description()
            self.__get_product_size()
            self.print_r(
                f"Product {self.product['name']} added for {self.float_to_fixed(float(time() - self.ttimer), 2)} sec")
        except Exception as error:
            self.print_r(f"{error}", "e")
        return self.product

    def __get_next_variation(self) -> None:
        """ Получение следующего артикула товара """
        self.print_r("Getting next product variation...")
        try:

            __size = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.size_item ul.size li")))
            __color = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.color_item ul.color li")))
            __glass = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.glass_item ul.glass li")))

            for __size_index in range(0, len(__size)):
                __size[__size_index].click()
                sleep(5)
                for __color_index in range(0, len(__color)):
                    __color[__color_index].click()
                    sleep(5)
                    for __glass_index in range(0, len(__glass)):
                        __glass[__glass_index].click()
                        sleep(5)
                        self.__close_jivo()
                        self.__get_data()
        except Exception as error:
            self.print_r(f"{error}", "e")

    def __get_product_name(self) -> None:
        """ Получение наименование товара """
        self.print_r("Getting product name...")
        try:
            self.product['name'] = self.current_product.find_element_by_css_selector("a span.name").text.split(" (")[0]
        except Exception as error:
            self.print_r(f"Name: {error}", "e")

    def __get_product_sku(self) -> None:
        """ Получение артикула товара """
        self.print_r("Getting product sku...")
        try:
            self.product['sku'] = self.current_product.find_element_by_css_selector(
                'div.articul-section span').text
        except Exception as error:
            self.print_r(f"Sku: {error}", "e")

    def __get_product_glass_and_color(self) -> None:
        """ Получение остекления продукта и цвета """
        self.print_r("Getting product glass and color...")
        try:
            __parent = self.driver.find_element_by_css_selector("a span.name")
            __color = self.current_product.find_element_by_css_selector("a span.name").text.split(" (")[1].capitalize()
            self.product['color'] = __color.split(")")[0]
        except Exception as error:
            self.print_r(f"Color: {error}", "e")

    def __get_product_price(self) -> None:
        """ Получение цены товара """
        self.print_r("Getting product price...")
        try:
            self.product['price'] = self.current_product.find_element_by_css_selector("div[itemprop='offers'] span.actual_price[itemprop='price']").get_attribute('content')
        except Exception as error:
            self.product['price'] = "7800"
            self.print_r(f"Price: {error}", "e")

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
            self.product['img'] = self.current_product.find_element_by_css_selector('a div.photo img').get_attribute('src')
        except Exception as error:
            self.print_r(f"Img: {error}", "e")

    def __get_product_size(self) -> None:
        """ Получение размера товара """
        self.print_r("Getting product size...")
        try:
            __parent = self.driver.find_element_by_css_selector(
                "div.size_item ul.size li.uf_size.active")
            self.product['size'] = __parent.text
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
