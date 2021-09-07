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
FILENAME = "dveri-rex"
PRODUCT_TYPE = "Дверь"
IS_BROWSER_HIDE = True
SITE_URLS = [
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=1", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=2", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=3", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=4", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=5", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=6", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=7", "Дверь"],
    ["https://dveri-rex.ru/katalog-dverei-rex/?page=8", "Дверь"],
]
MAX_PAGE_COUNT = 8
MAX_PRODUCTS_ON_ONE_PAGE = 36
