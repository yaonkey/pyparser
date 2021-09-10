import os

if os.name == "nt":
    SELENIUM_PATH = "assets\\geckodriver.exe"
    LOG_PATH = "logs\\"
elif os.name == 'posix':
    SELENIUM_PATH = "./assets/geckodriver"
    LOG_PATH = './logs/'
else:
    SELENIUM_PATH = str(input("Enter path to Selenium: "))
    LOG_PATH = str(input("Enter path for logs: "))
FILENAME = "oniks"
PRODUCT_TYPE = "Дверь"
IS_BROWSER_HIDE = True
SITE_URLS = [
    "https://www.oniks-dveri.ru/catalog/lite/",
    "https://www.oniks-dveri.ru/catalog/alum/",
    "https://www.oniks-dveri.ru/catalog/loft/",
    "https://www.oniks-dveri.ru/catalog/hi-tech/",
    "https://www.oniks-dveri.ru/catalog/neoclassic/",
    "https://www.oniks-dveri.ru/catalog/classic/",
    "https://www.oniks-dveri.ru/catalog/classic-premium/",
    "https://www.oniks-dveri.ru/catalog/standart/"
]
MAX_PAGE_COUNT = 6
MAX_PRODUCTS_ON_ONE_PAGE = 28
