import os

if os.name == "nt":
    SELENIUM_PATH = "assets\\geckodriver.exe"
elif os.name == 'posix':
    SELENIUM_PATH = "./assets/geckodriver"
else:
    SELENIUM_PATH = str(input("Enter path to Selenium: "))
FILENAME = "lesmastyle"
PRODUCT_TYPE = "Арка"
DEBUG = True
IS_BROWSER_HIDE = True

SITE_URLS = [
    "https://lesmastyle.ru/shop/arki/ellada/",
    "https://lesmastyle.ru/shop/arki/britanskaya/",
    "https://lesmastyle.ru/shop/arki/valencia/",
    "https://lesmastyle.ru/shop/arki/kazanka/",
    "https://lesmastyle.ru/shop/arki/milano/",
    "https://lesmastyle.ru/shop/arki/palermo/",
    "https://lesmastyle.ru/shop/arki/romanskaya/",
    "https://lesmastyle.ru/shop/arki/ufimka/"
]
