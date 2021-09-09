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
FILENAME = "t-lock"
PRODUCT_TYPE = "Фурнитура"
IS_BROWSER_HIDE = True

SITE_URLS = [
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_ab_bronza/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_ab_bronza/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_gr_grafit/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_gr_grafit/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_gp_latun/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_gp_latun/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_sg_mat_zoloto/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_sg_mat_zoloto/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_sn_mat_nikel/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_sn_mat_nikel/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_ac_med/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/p85c/p85c_50/korpus_zamka_plastic_p85c_50_cp_khrom/",
    "https://www.tlock.ru/catalog/zamki_vreznye/dlya_legkikh_dverey/m85c/m85c_50/korpus_zamka_magnet_m85c_50_cp_khrom/",
    "https://www.tlock.ru/catalog/ruchki_dvernye/dlya_razdvizhnykh_dverey/urban/sh010/ruchka_dlya_razdvizhnykh_dverey_sh010_urb_bl_26_chernyy_/",
    "https://www.tlock.ru/catalog/ruchki_dvernye/dlya_razdvizhnykh_dverey/urban/sh011/nabor_dlya_razdvizhnykh_dverey_sh011_urb_bl_26_chernyy_/",
    "https://www.tlock.ru/catalog/ruchki_dvernye/na_razdelnom_osnovanii/urban_slim/twin/ruchka_razdelnaya_twin_urs_ab_7_bronza/",
    "https://www.tlock.ru/catalog/ruchki_dvernye/na_razdelnom_osnovanii/urban/cube/ruchka_razdelnaya_cube_urb3_bpvd_black_77_voronenyy_nikel_chernyy/",
    "https://www.tlock.ru/catalog/petli/nakladnye_kartochnye/filter/e_color2-is-%D1%85%D1%80%D0%BE%D0%BC-or-%D1%87%D0%B5%D1%80%D0%BD%D1%8B%D0%B9%20%D0%BC%D0%B0%D1%82%D0%BE%D0%B2%D1%8B%D0%B9/producer-is-fuaro/series-is-4bb/apply/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/filter/e_maximum_load_3_loops-is-40%20%D0%BA%D0%B3-or-60%20%D0%BA%D0%B3/producer-is-armadillo/apply/",
]
MAX_PAGE_COUNT = 6
MAX_PRODUCTS_ON_ONE_PAGE = 28
