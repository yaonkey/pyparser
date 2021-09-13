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
FILENAME = "oniks-pere"
IS_BROWSER_HIDE = True
SITE_URLS = [
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-1/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-2/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-3/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-4/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-5/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-6/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-7/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-8/", "Межкомнатные перегородки"],
    ["https://www.oniks-dveri.ru/catalog/mezhkomnatnye-peregorodki/peregorodka-9/", "Межкомнатные перегородки"],
]
