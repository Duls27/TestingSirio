import numpy as np, pandas as pd, os
from tests import test_carica_esame, test_referta_esame
from selenium import webdriver
import classes

"""
test_manager handle all the test to do and write th final results
"""

def test_gateway (chrdriver: webdriver.Chrome, config_info: classes.configuration_info, lista_test_platofrom: pd.DataFrame, users: classes.users, folder_platform):
    """
    Like a gatway this function split all the test to the specific file test manager
    :param chrdriver: chrdrive of platform not logged
    :param config_info: config_info class
    :param lista_test_platofrom: DataFrame with test to do readed from bootstrap file
    :param users: users class
    :param folder_platform: folder path of the specific platform, to save results
    """
    for exam in lista_test_platofrom.keys():
        # Create folder for result of specific exam in platform
        folder_exam = str(folder_platform + "/" + exam)
        do_or_not=lista_test_platofrom.loc[exam]
        if not np.isnan(do_or_not):
            if exam == "carica_esame":
                print("\nInitializing test CARICA ESAME")
                #final_df_ce, sended_exam=test_carica_esame.send_more_exams(chrdriver=chrdriver, config_info=config_info, users= users, folder_exam=folder_exam)
            elif exam == "referta_esame":
                print("\nInitializing test REFERTA ESAME")
                test_referta_esame.report_more_exams(chrdriver=chrdriver, users=users, config_info=config_info, sended_exam=[1,0,0,0,1,1,1])#sended_exam da sostituire #[1,0,0,0,1,1,1]
            else:
                print("Exam not in list")


    #with pd.ExcelWriter(config_info.path_output, mode='a') as writer:
        #final_df.to_excel(writer, sheet_name='Sheet_name_3')