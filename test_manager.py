import numpy as np, pandas as pd
import support_functions, test_list,file_manager
from selenium import webdriver


#Test_gateway function is used for branching the code, takes from the bootstrap file all the information regarding
# the tests you want to run and following the columns in the excell file runs all the required tests, calling for
# each test the necessary functions.
#in case of more platfroms you can use each row for specify if do or not specific test for a specific platform
def test_gateway (chrdriver: webdriver.Chrome, path_bootstrap_excel, structure):
    df_test_list=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="lista_test")
    for exam in df_test_list:
        do_or_not=df_test_list.iloc[structure][exam]
        if exam == "carica_esami" and not np.isnan(do_or_not):
            carica_esami(chrdriver=chrdriver, path_bootstrap_excel=path_bootstrap_excel)
        else:
            print("Exam not in list")

#Carica_esami takes all the exams in excel sheet refered to the test CARICA_ESAMI and with this values call the functin to send exam

def carica_esami (chrdriver: webdriver.Chrome, path_bootstrap_excel):
    #retrieve user_info fromexcell
    df_info_users=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="users_info")
    #access as oper
    chrdriver = support_functions.enter_password_double_check(chrdriver,df_usr=df_info_users["opersite"])
    chrdriver.find_element_by_link_text("Carica").click()
    chrdriver.find_element_by_link_text("Esame").click()

    #retrieve info for test CARICA_ESAME, EXAMS_FILE_PATH, CONFIG from excell
    df_carica_esame=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="carica_esame")
    df_config=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="config_info")
    df_exams_path=file_manager.get_path_files_exams_from_folder_path(df_config.iloc[0]["path_exams"])

    for n_row in df_carica_esame.index:
        test_list.test_send_exam(chrdriver, df_carica_esame, n_row, df_exams_path, df_config)
        chrdriver.find_element_by_link_text("Carica").click()
        chrdriver.find_element_by_link_text("Esame").click()