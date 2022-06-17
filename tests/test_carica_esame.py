import time, pandas as pd, datetime, re, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as EX
import file_manager, classes

global n_row_CE

def send_more_exams (chrdriver: webdriver.Chrome, config_info: classes.configuration_info, users: classes.users, folder_exam):
    #access as oper
    chrdriver = users.login_opersite(chrdriver=chrdriver)

    #retrieve info for test CARICA_ESAME, EXAMS_FILE_PATH, CONFIG from excell
    df_carica_esame= pd.read_excel(config_info.path_input, sheet_name="carica_esame")

    df_exams_path=file_manager.get_path_files_from_folder_path(folder_path=config_info.path_exams)
    df_diary_path = file_manager.get_path_files_from_folder_path(folder_path=config_info.path_diaries)
    #set Df for final_result
    index_final=[]
    data_final=[]
    for n_row_CE in df_carica_esame.index:
        element = WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Carica")))
        element.click();
        #Check if carica esame is CaricaPDF
        if df_carica_esame.iloc[n_row_CE]["file_exam"] in ["pdf", "PDF"]:
            chrdriver.find_element_by_link_text("Esame PDF").click()
        else:
            chrdriver.find_element_by_link_text("Esame").click()

        #get expected errors and class to manipulate it
        err=classes.ce_errors()
        one_row_ce=df_carica_esame.iloc[n_row_CE]
        err_setted=set_expected_error(df_carica_esame= one_row_ce, err=err)
        #do Carica esame for one row
        err_final=carica_esame(chrdriver=chrdriver, one_row_ce= one_row_ce, df_exams_path=df_exams_path, df_diary_path=df_diary_path, config_info=config_info, err_setted=err_setted, folder_exam=folder_exam)

        index_final.append(str("CE" + str(n_row_CE)))
        data_final.append(err_final.get_flag_result())

        df_err_final = err_final.ce_errors_to_df()
        #In case of presence of errors save an additional csv with exp and eff errors
        if data_final[-1] == 1:
            df_err_final.to_csv(path_or_buf=str(folder_exam + "/" +str(n_row_CE) + "_exp_eff_table.csv"), sep=";")

    final_df = pd.DataFrame(data=data_final, index=index_final, columns=["CaricaEsame"])

    return final_df



        #write in csv insternalò for this test
        #write in results exp-eff

def carica_esame (chrdriver: webdriver.Chrome, one_row_ce: pd.DataFrame, df_exams_path: pd.DataFrame,df_diary_path: pd.DataFrame, config_info: classes.configuration_info, err_setted: classes.ce_errors, folder_exam):
        #################################### SENDING PARAM ############################################
        for key in one_row_ce.index:
            if one_row_ce.isnull().loc[key] and key != "datetime_files":
                continue
            elif key not in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_check_pacemaker", "inp_sel_sla","file_exam","datetime_files","file_diary"]:
                target = chrdriver.find_element(By.ID, key)
                target.clear()
                target.send_keys(str(one_row_ce.loc[key]))
            elif key == "inp_check_pacemaker":
                chrdriver.find_element(By.ID,key).click()
            elif key in ["inp_sel_sesso", "inp_sel_razza", "sel_tipiesame", "inp_sel_sla"]:
                chrdriver.find_element(By.XPATH,"// *[ @ id ='" + key + "']/option[text()='" + one_row_ce.loc[key] + "']").click()
            elif key == "file_exam":
                selected_exam = one_row_ce.loc[key]
                chooseFile = chrdriver.find_element(By.ID,key)
                if selected_exam != "borsam":
                    chooseFile.send_keys(df_exams_path.iloc[0][selected_exam])
                else:
                    files_for_borsam=df_exams_path.iloc[0][selected_exam] + " \n " + df_exams_path.iloc[1][selected_exam] + " \n " +  df_exams_path.iloc[2][selected_exam]
                    chooseFile.send_keys(str(files_for_borsam))
            elif key == "file_diary":
                selected_diary= one_row_ce.loc[key]
                chooseFile = chrdriver.find_element(By.ID,key)
                chooseFile.send_keys(df_diary_path.iloc[0][selected_diary])

            elif key == "datetime_files":

                if one_row_ce.loc[key] == 1:
                    conferma = WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='datetime_files']/div[2]/div/div[3]/button[2]")))
                    conferma.click()
                else:
                    annulla=WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@id='datetime_files']/div[2]/div/div[3]/button[1]")))
                    annulla.click()
        chrdriver.find_element_by_id("Invia").click()

        ################################# CHECK IF THERE ARE ERRORS #########################################
        try:
            #There is error banner?
            if chrdriver.find_element(By.XPATH,'//*[@id="id_div_informativo"]/div'):
                # Get text error
                alert_msg = chrdriver.find_element(By.XPATH, '//*[@id="id_div_informativo"]/div').text
        # No errors
        except:
            pass
        #if ther eis alert error, work on it
        if "alert_msg" in locals():
            #Control if is in known errors
            if alert_msg in err_setted.get_all_text():
                #Check if is expected
                for err in err_setted.__iter__():
                    if err.text == alert_msg:
                        #expected make screenshot
                        if err.exp == 0:
                            if not os.path.isdir(folder_exam):
                                os.mkdir(folder_exam)
                            err.eff=1
                            chrdriver.save_screenshot(filename=str(folder_exam + "/" +n_row_CE +"_not_expected.png"))
                            break
                        #expected, no screenshot
                        elif err.exp==1:
                            err.eff = 1
                            break

            #Is a new errror
            else:
                if not os.path.isdir(folder_exam):
                    os.mkdir(folder_exam)
                err_setted.new_error.text.append(alert_msg)
                #Make a screenshot to view it
                chrdriver.save_screenshot(filename=str(folder_exam+ "/" +n_row_CE +"_new_error_detected.png"))
                pass
        #Otherwise check that the file is send
        else:
            #check progress bar title for attending that platform send exam
            while True:
                progressCondition = chrdriver.find_element(By.ID,"id-modal-title").text
                if progressCondition == 'Invio dati esame in corso - 100%':
                    time.sleep(5)
                    break
                else:
                    time.sleep(0.1)

        return err_setted

def set_expected_error (df_carica_esame: pd.DataFrame, err: classes.ce_errors):

        # check mancanza_di_informazioni, list to control is write here
        for lbl in ["sel_tipiesame", "inp_nome_paziente", "inp_cognome_paziente", "inp_cf_paziente",
                    "inp_motivo_esame", "inp_terapia", "file_exam"]:
            if pd.isna(df_carica_esame.loc[lbl]):
                err.mancanzaInformazioni.exp=1
        #checks for every label
        for label in df_carica_esame.keys():
            value=df_carica_esame.loc[label]
            #check all data format
            #Control if data esame format is correct only if datetime_files in Nan otherwise i click choosing date proposed automatically by the file exam,
            #and in this case date is not useful
            if label == "inp_data_esame" and pd.isna(df_carica_esame.loc["datetime_files"]):
                try:
                    format = "%d-%m-%Y"
                    datetime.datetime.strptime(value, format)
                except:
                    err.dataEsameNV.exp=1

            if label == "inp_time_esame" and pd.isna(df_carica_esame.loc["datetime_files"]):
                try:
                    format = "%H:%M:%S"
                    datetime.datetime.strptime(value, format)
                except:
                    err.oraEsameNV.exp=1

            #check data_di_nascita format
            if label == "inp_data_di_nascita":
                try:
                    format = "%d-%m-%Y"
                    datetime.datetime.strptime(value, format)
                except:
                    err.dataNascitaNV.exp=1

            #check peso
            if label=="inp_peso_paziente":
                if re.search('[a-zA-Z]', str(value)):
                    err.pesoNV.exp=1

            #check altezza
            if label=="inp_altezza_paziente":
                if re.search('[a-zA-Z]', str(value)):
                    err.altezzaNV.exp=1

        return err

