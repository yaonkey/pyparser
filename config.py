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
    "https://www.tlock.ru/catalog/petli/nakladnye_kartochnye/4bb/4bb_100x75x2_5/petlya_universalnaya_4bb_100x75x2_5_cp_khrom/",
    "https://www.tlock.ru/catalog/petli/nakladnye_kartochnye/4bb/4bb_bl_100x75x2_5/petlya_universalnaya_4bb_bl_100x75x2_5_cp_khrom_blister/",
    "https://www.tlock.ru/catalog/petli/nakladnye_kartochnye/4bb/4bb_bl_100x75x2_5/petlya_universalnaya_4bb_bl_125x75x2_5_cp_khrom_blister/",
    "https://www.tlock.ru/catalog/petli/nakladnye_kartochnye/4bb/4bb_100x75x2_5/40843/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sg_matovoe_zoloto_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sn_matovyy_nikel_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sc_matovyy_khrom_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sc_matovyy_khrom_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sn_matovyy_nikel_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_sg_matovoe_zoloto_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_ab_bronza_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_ab_bronza_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_bl_chernyy_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_bl_chernyy_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_cp_8_khrom_lev_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/3d_ach/3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_architect_3d_ach_40_cp_8_khrom_prav_40_kg/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_wa/petlya_skrytoy_ustanovki_bez_regulirovki_universal_wa_sc_matovyy_khrom/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_9540un3d_sn_mat_nikel/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_universal_3d_ach_60_ab_bronza/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_9540un3d_bl_chernyy_/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_9540un3d_cp_khrom/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_9540un3d_sc_mat_khrom/",
    "https://www.tlock.ru/catalog/petli/skrytoy_ustanovki/universal/universal_3d_ach_40/petlya_skrytoy_ustanovki_s_3d_regulirovkoy_universal_3d_ach_60_sg_mat_zoloto/",
]
MAX_PAGE_COUNT = 6
MAX_PRODUCTS_ON_ONE_PAGE = 28
