import numpy as np, pandas as pd, os
from tests import test_carica_esame
from selenium import webdriver
import classes

#Test_gateway function is used for branching the code, takes from the bootstrap file all the information regarding
# the tests you want to run and following the columns in the excell file runs all the required tests, calling for
# each test the necessary functions.
#in case of more platfroms you can use each row for specify if do or not specific test for a specific platform
def test_gateway (chrdriver: webdriver.Chrome, config_info: classes.configuration_info, lista_test_platofrom: pd.DataFrame, users: classes.users, folder_platform):
    for exam in lista_test_platofrom.keys():
        # Create folder for result of specific exam in platform
        folder_exam = str(folder_platform + "/" + exam)
        do_or_not=lista_test_platofrom.loc[exam]
        if not np.isnan(do_or_not):
            if exam == "carica_esame":
                final_df_ce=test_carica_esame.send_more_exams(chrdriver=chrdriver, config_info=config_info, users= users, folder_exam=folder_exam)
            else:
                print("Exam not in list")

    print(final_df_ce)
    #with pd.ExcelWriter(config_info.path_output, mode='a') as writer:
        #final_df.to_excel(writer, sheet_name='Sheet_name_3')