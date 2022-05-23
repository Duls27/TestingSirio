import time

import support_functions
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#This function send one exam with specific label (set in excell document), the web driver must be inside the sending page
#INPUT: webdriver in sending page, Dataframe with data of label, path to sending exam, n_row_df is the number of excel row where take values
#OUTPUT: //
def test_send_exam (chrdriver: webdriver.Chrome, df_carica_esame: pd.DataFrame, n_row_df, df_file_test: pd.DataFrame, df_config: pd.DataFrame):
    for key in df_carica_esame.keys():
        if df_carica_esame.isnull().iloc[n_row_df][key] and key != "datetime_files":
            continue
        elif key not in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_check_pacemaker", "inp_sel_sla","file_exam","datetime_files"]:
            support_functions.normal_filling(chrdriver, key, str(df_carica_esame.iloc[n_row_df][key]))
        elif key == "inp_check_pacemaker":
            chrdriver.find_element_by_id(key).click()
        elif key in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_sel_sla"]:
            chrdriver.find_element_by_xpath("// *[ @ id ='" + key + "']/option[text()='" + df_carica_esame.iloc[n_row_df][key] + "']").click()
        elif key == "file_exam":
            if key == "file_exam":
                ext_file = df_carica_esame.iloc[n_row_df][key]
                chooseFile = chrdriver.find_element_by_id(key)
                if ext_file != "borsam":
                    chooseFile.send_keys(df_file_test.iloc[0][ext_file])
                else:
                    files_for_borsam=df_file_test.iloc[0][ext_file] + " \n " + df_file_test.iloc[1][ext_file] + " \n " +  df_file_test.iloc[2][ext_file]
                    chooseFile.send_keys(str(files_for_borsam))
        elif key == "datetime_files":
            WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='datetime_files']/div[2]/div/div[3]/button[1]" )))
            if df_carica_esame.iloc[n_row_df][key] == 1:
               chrdriver.find_element_by_xpath("//*[@id='datetime_files']/div[2]/div/div[3]/button[2]").click()
            else:
                chrdriver.find_element_by_xpath("//*[@id='datetime_files']/div[2]/div/div[3]/button[1]").click()

    chrdriver.find_element_by_id("Invia").click()

    # If sending exam there is an error, take a screenshot and pass
    if chrdriver.find_elements_by_xpath('//*[@id="id_div_informativo"]/div'):
        chrdriver.save_screenshot(filename= str(df_config.iloc[0]["path_folder_screenshot"]) + "/CaricaEsame_" + str(n_row_df) + ".png")
        return


#check progress bar title for attending that platform send exam
    while True:
        progressCondition = chrdriver.find_element_by_id("id-modal-title").text
        if progressCondition == 'Invio dati esame in corso - 100%':
            time.sleep(3)
            break
        else:
            time.sleep(0.1)

