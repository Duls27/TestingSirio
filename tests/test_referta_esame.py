import time, pandas as pd, datetime, re, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import classes


def report_more_exams (chrdriver: webdriver.Chrome, users: classes.users, config_info: classes.configuration_info, sended_exam: list):

    df_referta_esame = pd.read_excel(config_info.path_input, sheet_name="referta_esame", index_col="nome_cognome")
    df_referta_esame["sended"]=sended_exam
    users.login_cardio(chrdriver=chrdriver)
    #view all exam in table
    tutti = chrdriver.find_element(By.XPATH, "// *[ @ id = 'sel_sla'] / option[1]")
    actionChains = ActionChains(chrdriver)
    actionChains.double_click(tutti).perform()

    #save url of exams page
    url=chrdriver.current_url
    #return all element in table
    elements_in_table=chrdriver.find_elements(By.XPATH,"//*[@id='idTbodyEcgdarefertare']/*")
    #Insert in a list all 5th elements with tag td, extract names and surnames for each elemnt

    names_ids_exam_to_report={"names": [], "ids": []}
    for exam in elements_in_table.__iter__():
        name=exam.find_elements(By.TAG_NAME, "td")[5].text
        if name in df_referta_esame.index:
            #extract id of exam and name of patient ad save into dict
            names_ids_exam_to_report["ids"].append(exam.get_attribute("id"))
            names_ids_exam_to_report["names"].append(name)


    print(names_ids_exam_to_report)