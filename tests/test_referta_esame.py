import time

import numpy as np
import pandas as pd, os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import classes, file_manager
from tests.test_classes import classes_rf



def report_more_exams (chrdriver: webdriver.Chrome, users: classes.users, config_info: classes.configuration_info, sended_exam: list):

    df_referta_esame = pd.read_excel(config_info.path_input, sheet_name="referta_esame")
    url_platform=chrdriver.current_url
    #Check that exams are arrived, viewing from ADMIN
    df_referta_esame["stato"]=label_encoder(encode_param={'Refertabile': 1, "0": 0, 'Bloccato': -1},to_encode=sended_exam)
    df_exams_status = get_all_table_exams_POV_admin(chrdriver=chrdriver, users=users, dir_exams=config_info.path_exams)
    n_sende_exam=np.count_nonzero(a=sended_exam) #0 aren't sended
    # drop elemnt that are not sended (in sended_list=0), control if other exams are arrived
    df_arrived_exams=pd.merge(df_referta_esame, df_exams_status, on=["stato", "codice_fiscale"], how="inner")
    if n_sende_exam != df_arrived_exams.shape[0]:
        print("ERROR...  Number of sended exam is different from Admin POV")
        return 1
    """
    POP elemnt that are BLOCKED, in case of a specific test, remove POP
    """
    ids=df_arrived_exams[df_arrived_exams['stato']=="Bloccato"].index.values.tolist()
    df_arrived_exams.drop(ids, inplace=True)
    """
    Insert data of carica esame and associate to df_arrived exams
    """
    df_ce = pd.read_excel(config_info.path_input, sheet_name="carica_esame").drop_duplicates(subset="inp_cf_paziente")
    df_ex_to_report=pd.merge(df_arrived_exams, df_ce, left_on="codice_fiscale", right_on="inp_cf_paziente", how='inner').set_index('nome_cognome')

    chrdriver.get(url_platform)
    #Enter as Cardio for report exams
    users.login_cardio(chrdriver=chrdriver)
    #view all exam in table
    tutti = chrdriver.find_element(By.XPATH, "// *[ @ id = 'sel_sla'] / option[1]")
    actionChains = ActionChains(chrdriver)
    actionChains.double_click(tutti).perform()
    url_table=chrdriver.current_url
    #return all element in table
    elements_in_table=chrdriver.find_elements(By.XPATH,"//*[@id='idTbodyEcgdarefertare']/*")


    #REPORT EXAMS
    for exam in elements_in_table:
        tds=exam.find_elements(By.TAG_NAME, "td")
        name=tds[5].text
        str=tds[7].text
        if name in df_ex_to_report.index and str == users.struttura.name:
            type_exam=df_ex_to_report.loc[name]["file_exam"]
            actionChains = ActionChains(chrdriver)
            if type_exam=="PDF":
                actionChains.double_click(exam).perform()
                print("Manage pdf repor")
                chrdriver.get(url_table)
            elif type_exam=="BORSAM":
                actionChains.double_click(exam).perform()
                print("Manage borsam report")
                chrdriver.get(url_table)
            else:
                actionChains.double_click(exam).perform()
                print("manage all exams")
                chrdriver.get(url_table)

        #if control status for ech exam by admin, write code here (use another chdriver)
def report_generic_exam(chrdriver: webdriver.Chrome,):
    print()

def get_all_table_exams_POV_admin(chrdriver: webdriver.Chrome, users: classes.users, dir_exams: str):
    """
    Log as amdin and goes to the "Modifica stato esame" page, from this page select the exams of structure in users class,
    insert dates, from: oldest date between files in exam folder, to: today date.
    Return a datframe equal to the table in the page, only if all exams are arrived otherwise attend chnage of status.
    :param chrdriver:
    :param users:
    :param dir_exams:
    :return:
    """
    df_exams = file_manager.get_path_files_from_folder_path(dir_exams)
    exams=sum([df_exams[col].unique().tolist() for col in df_exams.columns],[]) #get only one unique value list from df_exams

    #get oldest file last modification date
    oldest_exam_date_TS=min([os.path.getmtime(exam) for exam in exams])
    oldest_exam_date = datetime.fromtimestamp(oldest_exam_date_TS).date().strftime("%d-%m-%Y").__str__()

    chrdriver=users.login_admin(chrdriver=chrdriver)
    chrdriver.find_element(By.LINK_TEXT, "Operazioni di Amministrazione").click()
    chrdriver.find_element(By.LINK_TEXT, "Modifica Stato Esame").click()

    inser_date_start = chrdriver.find_element(By.ID, "inp_date_from")
    inser_date_start.send_keys(oldest_exam_date)
    inser_date_end = chrdriver.find_element(By.ID, "inp_date_to")
    inser_date_end.send_keys(datetime.today().date().strftime("%d-%m-%Y").__str__())
    chrdriver.find_element(By.XPATH, "//*[@id='cc_table']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div").click()
    chrdriver.find_element(By.LINK_TEXT, users.struttura.name).click()

    chrdriver.find_element(By.ID, "search").click()

    #Create DataFrame that is similar to platform results table
    #Get one row at time of table
    table_admin=pd.DataFrame(columns=["DO_invio", "cardio",  "nome", "DO_refertazione", "DO_registrazione", "codice_fiscale", "struttura", "stato"])
    try:
        list_exams_t = chrdriver.find_elements(By.XPATH, "/html/body/div[4]/div/div/div/form/table[2]/tbody/tr")
        for idx, exam in enumerate(start=1, iterable=list_exams_t[1:]):  # first one is col_names
            tds = exam.find_elements(By.TAG_NAME, "td")
            new_row=[td.text for td in tds[1:8]]

            opt_status_t = exam.find_elements(By.TAG_NAME, "option")
            for opt in opt_status_t:
                if opt.get_attribute("selected"):
                    status_t = opt.text
                    start = time.time()
                    while status_t=="InLavorazione":
                        status_t=[op.text for op in exam.find_elements(By.TAG_NAME, "option") if op.get_attribute("selected")]
                        if time.time() - start > 59:
                            print(f"Exam{idx}  processing take more than ONE minute!")
                            break

                    break
            new_row.append(status_t)
            table_admin.loc[len(table_admin)]=new_row
    except:
        print("ERROR! No exams are related to the structure.")
    #table_admin.set_index('cf')
    return table_admin

def label_encoder(encode_param: dict, to_encode: list):
    """
    Simply takes dict with labels and corresponding value, and a ist that contains values to encode. Iterate on list_toencode
    and iterate on dictionary, when elem is equal to val_dict, append to return list
    :param encode_param:
    :param to_encode:
    :return:
    """
    return [lbl for elem in to_encode for val, lbl in zip(encode_param.values(), encode_param.keys()) if elem==val]








