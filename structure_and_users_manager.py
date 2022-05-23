import time, pandas as pd
from selenium import webdriver
import email_manager, support_functions, file_manager


def check_structure_existence (chrdriver: webdriver.Chrome ,path_bootstrap_excel):

    df_config_info=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name='config_info')
    df_users_info = file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name='users_info')
    #enter in platform as Admin
    chrdriver=support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])

    #######################################       PROJECT MANAJER       ################################################
    # check if exist refertatore
    '''
    chrdriver.find_element_by_link_text("Gestione Utenti").click()
    chrdriver.find_element_by_link_text("Project Manager").click()
    pms_name = chrdriver.find_element_by_id("id_utente").find_elements_by_tag_name("option")
    flag_create_pm = 1
    for pm in pms_name:
        if (pm.text.split(sep=" ")[3]) == df_users_info.iloc[0]["pm"]:
            flag_create_pm = 0
            break
    #if flag_create_pm == 1:
        create_pm(chrdriver=chrdriver, df_users_info=df_users_info, df_config_info=df_config_info)

    chrdriver = support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])#Enter as admin
    '''
    #####################################       CARDIO       ######################################################
    # check if exist refertatore
    chrdriver.find_element_by_link_text("Gestione Utenti").click()
    chrdriver.find_element_by_link_text("Refertatori").click()
    cardios_name = chrdriver.find_element_by_id("id_utente").find_elements_by_tag_name("option")
    flag_create_cardio = 1
    for cardio in cardios_name:
        if cardio.text.split(sep=" ")[3] == df_users_info.iloc[0]["cardio"]:
            flag_create_cardio = 0
            break
    if flag_create_cardio == 1:
        create_cardio(chrdriver=chrdriver, df_users_info=df_users_info, df_config_info=df_config_info)


    #########################################       OPER SITE       ####################################################
    # check if exist refertatore
    chrdriver.find_element_by_link_text("Gestione Utenti").click()
    chrdriver.find_element_by_link_text("Operatori Centri di raccolta").click()
    operssite = chrdriver.find_element_by_id("id_utente").find_elements_by_tag_name("option")
    flag_create_opersite = 1
    for opersite in operssite:
        if opersite.text == df_users_info.iloc[0]["opersite"]:
            flag_create_opersite = 0
            break
    if flag_create_opersite == 1:
        print("Crea funzone opersite")


    ###########################################       GRUPPO       #####################################################
    #check if exist gruppo
    chrdriver.find_element_by_link_text("Configura Strutture").click()
    chrdriver.find_element_by_link_text("Gruppi Strutture Territoriali").click()
    groups_name = chrdriver.find_element_by_id("id_gruppo_centri_raccolta_ecg").find_elements_by_tag_name("option")
    flag_create_group=1
    for group in groups_name:
        if group.text == df_users_info.iloc[0]["gruppo"]:
            flag_create_group=0
            break
    if flag_create_group == 1:
        print("Crea funxione Gruppo")


    return

######################################## PM FUNCTIONS ################################################################

def create_pm (chrdriver: webdriver.Chrome , df_config_info: pd.DataFrame, df_users_info: pd.DataFrame):

    email_manager.delete_all_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    fill_pm( chrdriver,df_config_info=df_config_info, df_users_info=df_users_info)
    time.sleep(3.0)
    mails = email_manager.get_google_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    pm_tmp_pwd=email_manager.get_tmp_pwd_from_emails(mails)
    #do_first acces
    keys=["username","password","nuova_password", "ridigita_nuova_password"]
    values=[df_users_info.iloc[0]["pm"], pm_tmp_pwd ,df_users_info.iloc[1]["pm"],df_users_info.iloc[1]["pm"]]
    for key,value in zip(keys, values):
        field = chrdriver.find_element_by_id(key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element_by_id("cambio_password").click()
    chrdriver.find_element_by_xpath("//*[@id='navbar']/ul/form/button").click()  # logout



def fill_pm (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):

    chrdriver.find_element_by_xpath("/html/body/div[4]/div/div/div/form[2]/input").click()
    fillig_dict=dict({"nome": "Selenium" ,"cognome": "pm","datadinascita": "20-11-1998","luogodinascita": "CardioCalm","indirizzo_email": df_config_info.iloc[0]["email"]  ,"numero_cellulare": "1234567890", "username": df_users_info.iloc[0]["pm"]})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element_by_id(key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.find_element_by_id("dati_sensibili").click()
    chrdriver.find_element_by_id("autenticazione-0").click()  #sirio internal user

    chrdriver.find_element_by_id("Salva").click()  # sirio
    chrdriver.find_element_by_xpath("//*[@id='navbar']/ul/form/button").click()


############################################# CARDIO FUNCTIONS ##########################################################

def create_cardio(chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):
    '''
    email_manager.delete_all_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    fill_cardio(chrdriver, df_config_info=df_config_info, df_users_info=df_users_info)
    time.sleep(3.0)
    '''
    mails = email_manager.get_google_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    pm_tmp_pwd = email_manager.get_tmp_pwd_from_emails(mails)
    # do_first acces
    keys = ["username", "password", "nuova_password", "ridigita_nuova_password"]
    values = [df_users_info.iloc[0]["cardio"], pm_tmp_pwd, df_users_info.iloc[1]["cardio"], df_users_info.iloc[1]["cardio"]]
    for key, value in zip(keys, values):
        field = chrdriver.find_element_by_id(key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element_by_id("cambio_password").click()
    chrdriver.find_element_by_xpath("//*[@id='navbar']/ul/form/button").click()  # logout


def fill_cardio (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):

    chrdriver.find_element_by_xpath("/html/body/div[4]/div/div/div/form[2]/input").click()
    fillig_dict = dict(
        {"nome": "Selenium", "cognome": "cardio", "datadinascita": "20-11-1998", "luogodinascita": "CardioCalm",
         "indirizzo_email": df_config_info.iloc[0]["email"], "numero_cellulare": "1234567890",
         "username": df_users_info.iloc[0]["cardio"], "n_iscriz_ordine": "1234"})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element_by_id(key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.find_element_by_id("delete_firma").click()
    chrdriver.find_element_by_id("supervisore").click()
    chrdriver.find_element_by_id("autenticazione-0").click()  # sirio internal user

    chrdriver.find_element_by_id("Salva").click()  # sirio
    chrdriver.find_element_by_xpath("//*[@id='navbar']/ul/form/button").click()