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

    df_referta_esame = pd.read_excel(config_info.path_input, sheet_name="referta_esame", index_col="codice_fiscale")
    df_carica_esame = pd.read_excel(config_info.path_input, sheet_name="carica_esame", index_col="inp_cf_paziente")
    df_referta_esame["sended"]=sended_exam

    #Before login as cardio, log as admin and control stratus of exams
    chrdriver=users.login_admin(chrdriver)
    chrdriver.find_element(By.LINK_TEXT, "Operazioni di Amministrazione").click()
    chrdriver.find_element(By.LINK_TEXT, "Modifica Stato Esame").click()
    url_find_exam=chrdriver.current_url

    for idx, cf in enumerate(df_referta_esame.index.tolist()):
        file_ext=df_carica_esame.iloc[idx]["file_exam"]
        file_exam=file_manager.get_specific_file_from_folder(folder=config_info.path_exams, extension=file_ext)
        ts_date=os.path.getmtime(file_exam)
        date_lastmodify_exam=datetime.fromtimestamp(ts_date).date().strftime("%d-%m-%Y").__str__()
        insert_cf=chrdriver.find_element(By.ID,"inp_cf")
        insert_cf.send_keys(cf)
        inser_date_start=chrdriver.find_element(By.ID,"inp_date_from")
        inser_date_start.send_keys(date_lastmodify_exam)
        inser_date_end = chrdriver.find_element(By.ID, "inp_date_to")
        inser_date_end.send_keys(date_lastmodify_exam)
        chrdriver.find_element(By.ID, "search").click()
        print("wait")

























"""
    users.login_cardio(chrdriver=chrdriver)
    #view all exam in table
    tutti = chrdriver.find_element(By.XPATH, "// *[ @ id = 'sel_sla'] / option[1]")
    actionChains = ActionChains(chrdriver)
    actionChains.double_click(tutti).perform()

    #return all element in table
    elements_in_table=chrdriver.find_elements(By.XPATH,"//*[@id='idTbodyEcgdarefertare']/*")
    #Insert in a list all 5th elements with tag td, extract names and surnames for each elemnt

    exams_to_report=classes_rf.exams_rf()

    #control if all sended exams are viewed by the cardio
    for exam in elements_in_table.__iter__():
        name=exam.find_elements(By.TAG_NAME, "td")[5].text
        if name in df_referta_esame["nome_cognome"].tolist():
            idx=df_referta_esame["nome_cognome"].tolist().index(name)
            if df_referta_esame.loc[idx]["sended"]==1:
                #extract id of exam and name of patient ad save into dict
                print(name)
                exams_to_report.ids.append(exam.get_attribute("id"))
                exams_to_report.names_surnames.append(name)
                exams_to_report.types.append(exam.find_elements(By.TAG_NAME, "td")[2].text)

            #control if all exams are arrived or not

    url = chrdriver.current_url
    #iterate for each exam and pass exams to specific function, discirminant is type of exam
    for id,type in zip(exams_to_report.ids, exams_to_report.types):
        type=type.split(sep="-")[0]
        element = WebDriverWait(chrdriver, 10).until(EC.element_to_be_clickable((By.ID, id)))
        actionChains.double_click(element).perform()

        if type == "PDF":
            report_pdf()


        chrdriver.get(url)


def report_pdf ():
    print("pdf")
"""