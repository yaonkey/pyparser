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
FILENAME = "oniks-pog"
# PRODUCT_TYPE = "Дверь Оникс"
IS_BROWSER_HIDE = True
SITE_URLS = [
    ["https://www.oniks-dveri.ru/catalog/dvernaya-korobka/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/nalichnik/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/kapiteli/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/podkapitelnye-planki/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/rozetki/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/komplekt-dlya-oformleniya-portala/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/dobor/", "Погонажные изделия"],
    ["https://www.oniks-dveri.ru/catalog/pritvornaya-planka/", "Погонажные изделия"],
]
