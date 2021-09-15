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
FILENAME = "luxor-dveri"
PRODUCT_TYPE = "Дверь"
IS_BROWSER_HIDE = False
SITE_URLS = [
    ["https://luxor-dveri.ru/catalog/mezhkomnatnye-dveri/?SHOW-BY=3", "Дверь"],
    ["https://luxor-dveri.ru/catalog/mezhkomnatnye-dveri/?SHOW-BY=3&PAGEN_1=2", "Дверь"],
]
MAX_PAGE_COUNT = 6
MAX_PRODUCTS_ON_ONE_PAGE = 28
