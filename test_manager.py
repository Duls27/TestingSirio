import file_manager
import numpy as np
import support_functions, test_list
from selenium import webdriver



def test_gateway (chrdriver: webdriver.Chrome, path_bootstrap_excel, n_row_to_test):
    df_test_list=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="lista_test")
    for exam in df_test_list:
        do_or_not=df_test_list.iloc[n_row_to_test][exam]
        if exam == "carica_esami" and not np.isnan(do_or_not):
            carica_esami(chrdriver=chrdriver, path_bootstrap_excel=path_bootstrap_excel)
        else:
            print("Exam not in list")

#Carica_esami takes all the exams in excel sheet refered to the test CARICA_ESAMI and with this values call the functin to send exam

def carica_esami (chrdriver: webdriver.Chrome, path_bootstrap_excel):
    #retrieve user_info fromexcell
    df_info_users=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="users_info")
    #access as oper
    chrdriver = support_functions.get_access(chrdriver,usr= df_info_users.iloc[0]['operatore'],pwd= df_info_users.iloc[1]['operatore'])
    chrdriver.find_element_by_link_text("Carica").click()
    chrdriver.find_element_by_link_text("Esame").click()

    #retrieve info for test CARICA_ESAME, EXAMS_FILE_PATH, CONFIGfrom excell
    df_carica_esame=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="carica_esame")

    for n_row in df_carica_esame.index:
        test_list.test_send_exam(chrdriver, df_carica_esame, n_row, df_exams_path, df_config)
        chrdriver.find_element_by_link_text("Carica").click()
        chrdriver.find_element_by_link_text("Esame").click()



