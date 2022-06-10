import numpy as np, pandas as pd
import support_functions,file_manager
from tests import test_carica_esame
from selenium import webdriver


#Test_gateway function is used for branching the code, takes from the bootstrap file all the information regarding
# the tests you want to run and following the columns in the excell file runs all the required tests, calling for
# each test the necessary functions.
#in case of more platfroms you can use each row for specify if do or not specific test for a specific platform
def test_gateway (chrdriver: webdriver.Chrome, path_bootstrap_excel, platform_index):
    df_test_list=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="lista_test")
    for exam in df_test_list.keys():
        #check in excel Lista_test which test we have to do, do_or_not is values in excel (1 = do it, Nan = not to do)
        do_or_not=df_test_list.iloc[platform_index][exam]
        if not np.isnan(do_or_not):
            if exam == "carica_esame":
                test_carica_esame.send_more_exams(chrdriver=chrdriver, path_bootstrap_excel=path_bootstrap_excel, platform_index=platform_index)
            else:
                print("Exam not in list")

#Carica_esami takes all the exams in excel sheet refered to the test CARICA_ESAMI and with this values call the functin to send exam

