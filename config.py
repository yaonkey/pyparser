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
    "https://lesmastyle.ru/shop/arki/ellada/0859583C-604C-1F9B-B5D1-4B067E848D4C",
    "https://lesmastyle.ru/shop/arki/ellada/ellada-belyj-yasen-900-1000-200-500-2450",
    "https://lesmastyle.ru/shop/arki/ellada/ellada-belenyj-dub-900-1000-200-500-2450",
    "https://lesmastyle.ru/shop/arki/britanskaya/britanskaya-mdf-700-1200-200-2250/",
    "https://lesmastyle.ru/shop/arki/britanskaya/britanskaya-belyj-yasen-700-1200-200-390-2250",
    "https://lesmastyle.ru/shop/arki/britanskaya/britanskaya-belenyj-dub-700-1200-200-390-2250",
    "https://lesmastyle.ru/shop/arki/valencia/valensiya-mdf-850-950-200-2150/",
    "https://lesmastyle.ru/shop/arki/valencia/valensiya-belyj-yasen-850-950-200-390-2150",
    "https://lesmastyle.ru/shop/arki/valencia/valensiya-belenyj-dub-850-950-200-390-2150",
    "https://lesmastyle.ru/shop/arki/kazanka/kazanka-mdf-800-900-200-2150/",
    "https://lesmastyle.ru/shop/arki/kazanka/kazanka-belyj-yasen-800-900-200-2150",
    "https://lesmastyle.ru/shop/arki/kazanka/kazanka-belenyj-dub-800-900-200-2150",
    "https://lesmastyle.ru/shop/arki/milano/milano-mdf-800-900-200-2150/",
    "https://lesmastyle.ru/shop/arki/milano/milano-belyj-yasen-800-900-200-390-2150",
    "https://lesmastyle.ru/shop/arki/milano/milano-belenyj-dub-800-900-200-390-2150",
    "https://lesmastyle.ru/shop/arki/palermo/milano-mdf-700-1300-so-svodorasshiritelem-200-2150/",
    "https://lesmastyle.ru/shop/arki/palermo/palermo-belyj-yasen-700-1300-so-svodorasshiritelem-200-390-2150",
    "https://lesmastyle.ru/shop/arki/palermo/palermo-belenyj-dub-700-1300-so-svodorasshiritelem-200-390-2150",
    "https://lesmastyle.ru/shop/arki/romanskaya/romanskaya-mdf-800-900-200-2150/",
    "https://lesmastyle.ru/shop/arki/romanskaya/romanskaya-belyj-yasen-800-900-200-390-2150",
    "https://lesmastyle.ru/shop/arki/romanskaya/romanskaya-massiv-sosna-800-900-70-190-2150",
    "https://lesmastyle.ru/shop/arki/romanskaya/romanskaya-belenyj-dub-800-900-200-390-2150",
    "https://lesmastyle.ru/shop/arki/ufimka/ufimka-mdf-800-190-2100/",
    "https://lesmastyle.ru/shop/arki/ufimka/ufimka-belyj-yasen-800-190-2100",
    "https://lesmastyle.ru/shop/arki/ufimka/ufimka-belenyj-dub-800-190-2100"
]
