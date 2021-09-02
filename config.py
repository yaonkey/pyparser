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
FILENAME = "dveridk"
PRODUCT_TYPE = "Двери"
DEBUG = True
IS_BROWSER_HIDE = True

SITE_URLS = [
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_lion_temnyy_orekh/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_milan_temnyy_orekh/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_porta_temnyy_orekh/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_novello_albero_brash/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_venge/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_konsul_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_florentsiya_zolotoy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_florentsiya_temnyy_orekh/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_florentsiya_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_ekstra_venge/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_ekstra_listvennitsa_bezhevaya/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_z3k_venge/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_z3k_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_ultra_venge/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_termal_ultra_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_s3k_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_s3k_listvennitsa_seraya/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_3k_venge/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_siti_3k_belenyy_dub/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_rubikon_100_tsarga_sandal_belyy/",
    "https://dveridk.ru/catalog/vkhodnye_metallicheskie_dveri/vkhodnaya_dver_rubikon_100_tsarga_venge/"
]
