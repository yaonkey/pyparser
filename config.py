import os

if os.name == "nt":
    SELENIUM_PATH = "assets\\geckodriver.exe"
    LOG_PATH = "logs\\"
elif os.name == 'posix':
    SELENIUM_PATH = "./assets/geckodriver"
    LOG_PATH = './logs/debug.log'
else:
    SELENIUM_PATH = str(input("Enter path to Selenium: "))
    LOG_PATH = str(input("Enter path for logs: "))
FILENAME = "lesmastyle"
PRODUCT_TYPE = "Арка"
DEBUG = True
IS_BROWSER_HIDE = True

SITE_URLS = [
    ["https://lesmastyle.ru/shop/arki/details-for-arches/stykovochnye-planki-rejki/stykovochnaya-planka/stykovochnaya-planka-belenyj-dub", ""]
]
