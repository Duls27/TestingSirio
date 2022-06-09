import time, pandas as pd, numpy as np, datetime, re, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as EX
import support_functions, file_manager


def send_more_exams (chrdriver: webdriver.Chrome, path_bootstrap_excel, platform):
    #retrieve user_info fromexcell
    df_info_users=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="users_info")
    #access as oper
    chrdriver = support_functions.enter_password_double_check(chrdriver,df_usr=df_info_users["opersite"])

    #retrieve info for test CARICA_ESAME, EXAMS_FILE_PATH, CONFIG from excell
    df_carica_esame=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="carica_esame")
    df_config=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name="config_info")
    path=df_config.iloc[platform]["path_exams"]
    df_exams_path=file_manager.get_path_files_from_folder_path(folder_path=path)
    path=df_config.iloc[platform]["path_diaries"]
    df_diary_path = file_manager.get_path_files_from_folder_path(folder_path=path)

    #get two dataframes with expected and effective(empty) errors
    df_expected_errors=get_expected_errors_carica_esame(df_carica_esame=df_carica_esame)

    for n_row in df_carica_esame.index:
        element = WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Carica")))
        element.click();
        #Check if carica esame is CaricaPDF
        if df_carica_esame.iloc[n_row]["file_exam"] in ["pdf", "PDF"]:
            chrdriver.find_element_by_link_text("Esame PDF").click()
        else:
            chrdriver.find_element_by_link_text("Esame").click()

        df_effective_errors=carica_esame(platform,chrdriver, df_carica_esame, n_row, df_exams_path, df_diary_path, df_config, df_expected_errors)

#This function send one exam with specific label (set in excell document), the web driver must be inside the sending page
#INPUT: webdriver in sending page, Dataframe with data of label, path to sending exam, n_row_df is the number of excel row where take values
#OUTPUT: //
def carica_esame (platform,chrdriver: webdriver.Chrome, df_carica_esame: pd.DataFrame, n_row_df, df_file_test: pd.DataFrame,df_diary_path: pd.DataFrame, df_config: pd.DataFrame, df_expected_errors: pd.DataFrame):

    #get empty DF wit errors as colnames for saving errors that are not expected
    df_effective_errors=get_df_possible_errors()
    #This class contain al posssible error eand values expected
    try:
        for key in df_carica_esame.keys():
            if df_carica_esame.isnull().iloc[n_row_df][key] and key != "datetime_files":
                continue
            elif key not in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_check_pacemaker", "inp_sel_sla","file_exam","datetime_files","file_diary"]:
                support_functions.normal_filling(chrdriver, key, str(df_carica_esame.iloc[n_row_df][key]))
            elif key == "inp_check_pacemaker":
                chrdriver.find_element(By.ID,key).click()
            elif key in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_sel_sla"]:
                chrdriver.find_element(By.XPATH,"// *[ @ id ='" + key + "']/option[text()='" + df_carica_esame.iloc[n_row_df][key] + "']").click()
            elif key == "file_exam":
                selected_exam = df_carica_esame.iloc[n_row_df][key]
                chooseFile = chrdriver.find_element(By.ID,key)
                if selected_exam != "borsam":
                    chooseFile.send_keys(df_file_test.iloc[0][selected_exam])
                else:
                    files_for_borsam=df_file_test.iloc[0][selected_exam] + " \n " + df_file_test.iloc[1][selected_exam] + " \n " +  df_file_test.iloc[2][selected_exam]
                    chooseFile.send_keys(str(files_for_borsam))
            elif key == "file_diary":
                selected_diary= df_carica_esame.iloc[n_row_df][key]
                chooseFile = chrdriver.find_element(By.ID,key)
                chooseFile.send_keys(df_diary_path.iloc[0][selected_diary])

            elif key == "datetime_files":

                if df_carica_esame.iloc[n_row_df][key] == 1:
                    conferma = WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='datetime_files']/div[2]/div/div[3]/button[2]")))
                    conferma.click()
                else:
                    annulla=WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='datetime_files']/div[2]/div/div[3]/button[1]")))
                    annulla.click()

        chrdriver.find_element_by_id("Invia").click()

        ################################# CHECK IF THERE ARE ERRORS #########################################

        #If exist id_informativo means there is an error, otherwise id_informativo become visibible only after correnct send of exam
        #So check if after sending click exist error, if exist flag=1 and after check if es an expected error or not

        #Check FLAG
        flag_id_informativo=0
        try:
            if chrdriver.find_element(By.XPATH,'//*[@id="id_div_informativo"]/div'):
                flag_id_informativo=1
        except:
            pass

        #If FLAG is == 1, error!, check if is expected otherwise do something...
        if flag_id_informativo==1:
            alert_msg= chrdriver.find_element(By.ID,"id_div_informativo").text
            #check if the error is expected or not, if not screenshot it and save the error
            try:
                is_expected=df_expected_errors.iloc[n_row_df][alert_msg]
                #if is exected (==1) pass otherwise save into effective errorrs and make screenshot
                if is_expected == 1:
                    pass
                else:
                    #Create if not exist folder for Carica Esame Test Screenshot
                    path_folder_screenshot_CaricaEsame=str(df_config.iloc[0]["path_folder_screenshot"]) + "/CaricaEsame_"
                    if not os.path.exists(path_folder_screenshot_CaricaEsame):
                        os.mkdir(path_folder_screenshot_CaricaEsame)
                    # Create if not exist folder for Carica Esame Test Screenshot of specific Platform
                    path_folder_screenshot_CaricaEsame_platform= str(path_folder_screenshot_CaricaEsame + str(platform))
                    if not os.path.exists(path_folder_screenshot_CaricaEsame_platform):
                        os.mkdir(path_folder_screenshot_CaricaEsame_platform)
                    #save error msg in dataframe and save screeshot
                    df_effective_errors._set_value(n_row_df, alert_msg, 1)
                    chrdriver.save_screenshot(filename=str(path_folder_screenshot_CaricaEsame_platform + str(n_row_df) + ".png"))

            #if the error is new (no tin list of expected), insert it in the list of errors and set vallue to one
            #
            #!!!!!!!!!!!!!!!
            # if the error does not exist, correct the code by entering the error text in (get_df_possible_errors) and then enter as detect it in (get_expected_errors_carica_esame)
            #!!!!!!!!!!!!!!
            #
            #At the moment add it as column in Dataframe end return all errors, print it
            except:
                df_effective_errors.insert(column=alert_msg, value=1)
                print("There is a NEW ERROR, is saved in Errors DataFrame, you have to add it at the errors: check comment in function Carica_Esame ")
                chrdriver.save_screenshot(filename=str(path_folder_screenshot_CaricaEsame_platform + str(n_row_df) + ".png"))

        ################## CHECK IF SENDING ESAME ENDED ##############################

        #If there are no alert messages, check send exam. Checking if variable exist in local variables
        if "alert_msg" not in locals():
            #check progress bar title for attending that platform send exam
            while True:
                progressCondition = chrdriver.find_element(By.ID,"id-modal-title").text
                if progressCondition == 'Invio dati esame in corso - 100%':
                    time.sleep(5)
                    break
                else:
                    time.sleep(0.1)

    ##################################### HANDLE EXCEPTIONS #########################################

    except EX.NoSuchElementException as exception:
        print("No element ex: \n" + "Carica esame, coordinates of values that raise error, n_row: "+ str(n_row_df))
        print(exception.msg)
        print(exception.args)

    except EX.UnexpectedAlertPresentException as exception:
        print("Carica esame, Presence of alert unexpected: \n")
        print(exception.msg)
        print(exception.args)

    except EX.ElementClickInterceptedException as exception:
        print("Click excpetion: \n" + "Carica esame, coordinates of values that raise error, n_row: "+ str(n_row_df))
        print(exception.msg)
        print(exception.args)

    return df_effective_errors

#return an empty DataFrame with Possibe errors of CaricaEsame (POSSIBLE_ERROS are col_names)
def get_df_possible_errors():
    POSSIBLE_ERRORS = ["Mancanza di informazioni necessarie per il caricamento dell'esame",
                       "Data esame non valida, formato data dd-mm-aaaa",
                       "Ora esame non valida",
                       "Data di nascita non valida, formato data dd-mm-aaaa",
                       "Peso non valido",
                       "Altezza non valida"]

    return pd.DataFrame(columns=POSSIBLE_ERRORS)

#POSSIBLE_ERRORS is the list of messages that the platform could retrieve in case of sending exams
#using this list the function retrieve two DataFrame, EXPECTED ERRORS inserting in the DataFrame wich are the expected errors for every row of df_carica_esame and EFFECTIVE_ERROS wich is the same DataFrame but empty
#If you insert another errors you have to manage it below, otherwise the function doesn't detect the EXPECTED ERROR
def get_expected_errors_carica_esame (df_carica_esame: pd.DataFrame):

    df_expected_errors = get_df_possible_errors()

    #FILL DATAFRAME EXPECTED TESTING INPUT VALUES
    #values that could retrieve Mancanza di informazioni necessarie
    for row in df_carica_esame.index:

        # check mancanza_di_informazioni, list to control is write here
        for lbl in ["sel_tipiesame", "inp_nome_paziente", "inp_cognome_paziente", "inp_cf_paziente",
                    "inp_motivo_esame", "inp_terapia", "file_exam"]:
            if pd.isna(df_carica_esame.iloc[row][lbl]):
                df_expected_errors._set_value(row, "Mancanza di informazioni necessarie per il caricamento dell'esame",
                                           1)
        #checks for every label
        for label in df_carica_esame.keys():
            value=df_carica_esame.iloc[row][label]
            #check all data format
            #Control if data esame format is correct only if datetime_files in Nan otherwise i click choosing date proposed automatically by the file exam,
            #and in this case date is not useful
            if label == "inp_data_esame" and pd.isna(df_carica_esame.iloc[row]["datetime_files"]):
                try:
                    format = "%d-%m-%Y"
                    datetime.datetime.strptime(value, format)
                except:
                    df_expected_errors._set_value(row, "Data esame non valida, formato data dd-mm-aaaa",1)

            if label == "inp_time_esame" and pd.isna(df_carica_esame.iloc[row]["datetime_files"]):
                try:
                    format = "%H:%M:%S"
                    datetime.datetime.strptime(value, format)
                except:
                    df_expected_errors._set_value(row, "Ora esame non valida", 1)

            #check data_di_nascita format
            if label == "inp_data_di_nascita":
                try:
                    format = "%d-%m-%Y"
                    datetime.datetime.strptime(value, format)
                except:
                    df_expected_errors._set_value(row, "Data di nascita non valida, formato data dd-mm-aaaa", 1)

            #check peso
            if label=="inp_peso_paziente":
                if re.search('[a-zA-Z]', str(value)):
                    df_expected_errors._set_value(row, "Peso non valido", 1)

            #check altezza
            if label=="inp_altezza_paziente":
                if re.search('[a-zA-Z]', str(value)):
                    df_expected_errors._set_value(row, "Altezza non valida", 1)

    return df_expected_errors