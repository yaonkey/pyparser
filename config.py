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
FILENAME = "vk"
PRODUCT_TYPE = ""
IS_BROWSER_HIDE = True
SITE_URLS = [
    ["https://vk.com/market-161176754?section=album_13&w=product-161176754_4978986%2Fquery", "Изделия из эпоксидной смолы"],
    ["https://vk.com/market-161176754?section=album_11&w=product-161176754_3695971%2Fquery", "Одежда для игрушек"],
    ["https://vk.com/market-161176754?section=album_10&w=product-161176754_4684104%2Fquery", "Брелоки"],
    ["https://vk.com/market-161176754?section=album_9&w=product-161176754_4161835%2Fquery", "Товары для животных"],
    ["https://vk.com/market-161176754?section=album_8&w=product-161176754_4266881%2Fquery", "Одежда"],
    ["https://vk.com/market-161176754?section=album_7&w=product-161176754_4005306%2Fquery", "Пледы"],
    ["https://vk.com/market-161176754?section=album_2&w=product-161176754_3512818%2Fquery", "Фенечки"],
    ["https://vk.com/market-161176754?section=album_4&w=product-161176754_5009238%2Fquery", "Вязаные игрушки"],
    ["https://vk.com/market-161176754?section=album_2&w=product-161176754_3512818%2Fquery", "Ловцы снов"],
    ["https://vk.com/market-161176754?section=album_6&w=product-161176754_3578119%2Fquery", "Вязаные чехлы"],
    ["https://vk.com/market-161176754?section=album_3&w=product-161176754_4266883%2Fquery", "Нашивки"],
    ["https://vk.com/uslugi-161176754?section=album_14&w=product-161176754_5009536%2Fquery", "Описания"],
]
