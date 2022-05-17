import file_manager
import support_functions, test_list
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def test_gateway (chrdriver: webdriver.Chrome, path_bootstrap_excel):
    df_test_list=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="lista_test")
    for key in df_test_list:
        if key == "carica_esami":
            carica_esami()
        else:
            print("shh")

#Carica_esami takes all the exams in excel sheet refered to the test CARICA_ESAMI and with this values call the functin to send exam

def carica_esami (chrdriver: webdriver.Chrome, path_bootstrap_excel):
    #access as oper
    chrdriver = support_functions.get_access(chrdriver, df_users.iloc[0]['oper'], df_users.iloc[1]['oper'])
    chrdriver.find_element_by_link_text("Carica").click()
    chrdriver.find_element_by_link_text("Esame").click()

    for n_row in df_carica_esame.index:
        test_list.test_send_exam(chrdriver, df_carica_esame, n_row, df_exams_path, df_config)
        chrdriver.find_element_by_link_text("Carica").click()
        chrdriver.find_element_by_link_text("Esame").click()



