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

    df_referta_esame = pd.read_excel(config_info.path_input, sheet_name="referta_esame", index_col="codice_fiscale")
    df_carica_esame = pd.read_excel(config_info.path_input, sheet_name="carica_esame", index_col="inp_cf_paziente")
    df_referta_esame["sended"]=sended_exam
    get_all_exams_POV_admin(chrdriver=chrdriver, users=users, dir_exams=config_info.path_exams)



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


def get_all_exams_POV_admin(chrdriver: webdriver.Chrome, users: classes.users, dir_exams: str):
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

    for str in chrdriver.find_elements(By.XPATH,"//*[@id='cc_table']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/ul/li"):
        span=str.find_elements(By.XPATH, "//a/span[1]")
        print(span.text)
        #could find name of str

    chrdriver.find_element(By.ID, "search").click()
    # get list of exams finded in platform

#/html/body/div[4]/div/div/div/form/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div/div/ul/li[9]/a/span[1]
"""
    try:
        list_exams_t = chrdriver.find_elements(By.XPATH, "/html/body/div[4]/div/div/div/form/table[2]/tbody/tr")
        for exam in list_exams_t[1:]:  # first one is col_names
            tds = exam.find_elements(By.TAG_NAME, "td")
            cf_t = tds[6].text
            str_t = tds[7].text
            opt_status_t = exam.find_elements(By.TAG_NAME, "option")
            for opt in opt_status_t:
                if opt.get_attribute("selected"):
                    status_t = opt.text
                    break
"""










