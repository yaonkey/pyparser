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
FILENAME = "oniks-furn"
IS_BROWSER_HIDE = True
SITE_URLS = [
    ["https://www.oniks-dveri.ru/catalog/furnitura-morelli/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/zamok-santekhnicheskiy/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/zamok-pod-tsilindr/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/petli/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/ruchki/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/rigel/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/alyuminievaya-kromka/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/otboynaya-plastina/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/avtoprog/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/ventilyatsionnaya-reshetka/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/dovodchik/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/skrytyy-magnitnyy-upor/", "Фурнитура"],
    ["https://www.oniks-dveri.ru/catalog/furnitura-dlya-steklyannykh-dverey/", "Фурнитура"],
]
