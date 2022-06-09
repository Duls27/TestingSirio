import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import email_manager, support_functions, file_manager
import selenium.common.exceptions as ex


def check_structure_existence (chrdriver: webdriver.Chrome ,path_bootstrap_excel, struttura):
    try:
        df_config_info=file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name='config_info')
        df_users_info = file_manager.get_info_from_excel(path_bootstrap=path_bootstrap_excel, sheet_name='users_info')
        #enter in platform as Admin
        chrdriver=support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])

        ###########################################       GRUPPO       #####################################################
        # check if exist gruppo
        chrdriver.find_element_by_link_text("Configura Strutture").click()
        chrdriver.find_element_by_link_text("Gruppi Strutture Territoriali").click()
        groups_name = chrdriver.find_element(By.ID,"id_gruppo_centri_raccolta_ecg").find_elements(By.TAG_NAME,"option")
        flag_create_group = 1
        for group in groups_name:
            if df_users_info.iloc[0]["gruppo"] in group.text:
                flag_create_group = 0
                break
        if flag_create_group == 1:
            create_gruppo(chrdriver=chrdriver, df_users_info=df_users_info)
            chrdriver.get(struttura)
            chrdriver = support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])  # Enter as admin

        #######################################       PROJECT MANAJER       ################################################
        # check if exist refertatore

        chrdriver.find_element(By.LINK_TEXT,"Gestione Utenti").click()
        chrdriver.find_element(By.LINK_TEXT,"Project Manager").click()
        pms_name = chrdriver.find_element(By.ID,"id_utente").find_elements_by_tag_name("option")
        flag_create_pm = 1
        for pm in pms_name:
            if df_users_info.iloc[0]["pm"] in pm.text:
                flag_create_pm = 0
                break
        if flag_create_pm == 1:
            create_pm(chrdriver=chrdriver, df_users_info=df_users_info, df_config_info=df_config_info, struttura=struttura)
            chrdriver.get(struttura)
            chrdriver = support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])#Enter as admin


        #########################################       OPER SITE       ####################################################
        # check if exist refertatore
        chrdriver.find_element_by_link_text("Configura Strutture").click()
        chrdriver.find_element_by_link_text("Territoriali").click()
        try:
            territoriali = chrdriver.find_element_by_id("id_centro_raccolta").find_elements_by_tag_name("option")
        except:
            territoriali = chrdriver.find_element_by_id("id_struttura_territoriale").find_elements_by_tag_name("option") #MM

        flag_create_opersite = 1
        for territoriale in territoriali:
            if str(df_users_info.iloc[0]["struttura"]) in territoriale.text:
                flag_create_opersite = 0
                break

        if flag_create_opersite == 1:
            create_territoriale(chrdriver=chrdriver, df_users_info=df_users_info, df_config_info=df_config_info, struttura=struttura)
            chrdriver.get(struttura)
            chrdriver = support_functions.enter_password_double_check(chrdriver, df_users_info["admin"])  # Enter as admin

       #####################################       CARDIO       ######################################################
        # check if exist refertatore
        chrdriver.find_element_by_link_text("Gestione Utenti").click()
        chrdriver.find_element_by_link_text("Refertatori").click()
        cardios_name = chrdriver.find_element_by_id("id_utente").find_elements_by_tag_name("option")

        flag_create_cardio = 1
        for cardio in cardios_name:
            if df_users_info.iloc[0]["cardio"] in cardio.text:
                flag_create_cardio = 0
                break
        if flag_create_cardio == 1:
            create_cardio(chrdriver=chrdriver, df_users_info=df_users_info, df_config_info=df_config_info, struttura=struttura)
            chrdriver.get(struttura)
    except ex.NoSuchElementException as no_elem_ex:
        print("Element selected is not present: \n" + no_elem_ex.msg + "\n" + no_elem_ex.args)

    except ex.TimeoutException as time_ex:
        print("Something goes wrong, timeout excpetion: \n" + time_ex.msg)

    except ex.UnexpectedAlertPresentException as alert_ex:
        print("Alert excpetion: \n" + alert_ex.msg)
        pass


################################## FUNCTIONS FOR CREATION OF USERS #################################################


####################################### PM FUNCTIONS ###############################################################

def create_pm (chrdriver: webdriver.Chrome , df_config_info: pd.DataFrame, df_users_info: pd.DataFrame, struttura):

    #email_manager.delete_all_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    fill_pm( chrdriver,df_config_info=df_config_info, df_users_info=df_users_info)
    email_manager.await_receipt_of_email(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    mails = email_manager.get_google_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    pm_tmp_pwd=email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(struttura)
    #do_first acces
    keys=["username","password","nuova_password", "ridigita_nuova_password"]
    values=[df_users_info.iloc[0]["pm"], pm_tmp_pwd ,df_users_info.iloc[1]["pm"],df_users_info.iloc[1]["pm"]]
    for key,value in zip(keys, values):
        field = chrdriver.find_element_by_id(key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element(By.ID,"cambio_password").click()



def fill_pm (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):
    chrdriver.find_element_by_xpath('//input[@value="Nuovo Project Manager"]').click()
    fillig_dict=dict({"nome": "Selenium" ,"cognome": "pm","datadinascita": "20-11-1998","luogodinascita": "CardioCalm","indirizzo_email": df_config_info.iloc[0]["email"]  ,"numero_cellulare": "1234567890", "username": df_users_info.iloc[0]["pm"]})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element_by_id(key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.find_element_by_id("dati_sensibili").click()
    chrdriver.find_element_by_id("autenticazione-0").click()  #sirio internal user

    gruppo = chrdriver.find_element_by_xpath("//*[@id='gruppo_centri_raccolta_ecg']/option[text()= '{}']".format(df_users_info.iloc[0]["gruppo"]))
    gruppo.click()

    chrdriver.find_element_by_id("Salva").click()  # sirio



########################################## CARDIO FUNCTIONS ##########################################################

def create_cardio(chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame, struttura):

    email_manager.delete_all_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    fill_cardio(chrdriver, df_config_info=df_config_info, df_users_info=df_users_info)
    email_manager.await_receipt_of_email(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])

    mails = email_manager.get_google_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    pm_tmp_pwd = email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(struttura)
    # do_first acces
    keys = ["username", "password", "nuova_password", "ridigita_nuova_password"]
    values = [df_users_info.iloc[0]["cardio"], pm_tmp_pwd, df_users_info.iloc[1]["cardio"], df_users_info.iloc[1]["cardio"]]
    for key, value in zip(keys, values):
        field = chrdriver.find_element_by_id(key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element(By.ID,"cambio_password").click()


def fill_cardio (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):

    chrdriver.find_element(By.XPATH,'//input[@value="Nuovo Cardiologo"]').click()
    fillig_dict = dict(
        {"nome": "Selenium", "cognome": "cardio", "datadinascita": "20-11-1998", "luogodinascita": "CardioCalm",
         "indirizzo_email": df_config_info.iloc[0]["email"], "numero_cellulare": "1234567890",
         "username": df_users_info.iloc[0]["cardio"], "n_iscriz_ordine": "1234"})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element(By.ID,key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.chrdriver.find_element(By.ID,"delete_firma").click()
    chrdriver.chrdriver.find_element(By.ID,"supervisore").click()
    chrdriver.chrdriver.find_element(By.ID,"autenticazione-0").click()  # sirio internal user

    gruppo = chrdriver.chrdriver.find_element(By.XPATH,"//*[@id='gruppo_centri_raccolta_ecg']/option[text()= '{}']".format(df_users_info.iloc[0]["gruppo"]))
    gruppo.click()

    select = Select(chrdriver.chrdriver.find_element(By.ID,"tipi_esame"))
    n_servizi = len(select.options)
    from_element = chrdriver.chrdriver.find_element(By.ID,"//*[@id='tipi_esame']/option[1]")
    to_element = chrdriver.chrdriver.find_element(By.ID,"//*[@id='tipi_esame']/option[{}]".format(n_servizi))
    action = ActionChains(chrdriver)
    action.click_and_hold(from_element).move_to_element(to_element).perform()


    chrdriver.chrdriver.find_element(By.ID,"Salva").click()  # sirio


########################################### GRUPPO FUNCTIONS ########################################################

def create_gruppo (chrdriver: webdriver.Chrome, df_users_info: pd.DataFrame):

    chrdriver.chrdriver.find_element(By.ID,"Nuovo").click()
    name=chrdriver.chrdriver.find_element(By.ID,"nome")
    name.send_keys(df_users_info.iloc[0]["gruppo"])
    chrdriver.chrdriver.find_element(By.ID,"Salva").click()


####################################### TERRITORIALE E OPER FUNCTIONS ##############################################

def create_territoriale (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame, struttura):

    email_manager.delete_all_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    fill_territoriale(chrdriver, df_config_info=df_config_info, df_users_info=df_users_info)
    email_manager.await_receipt_of_email(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    mails = email_manager.get_google_emails(df_config_info.iloc[0]["email"], df_config_info.iloc[1]["email"])
    pm_tmp_pwd = email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(struttura)
    # do_first acces
    keys = ["username", "password", "nuova_password", "ridigita_nuova_password"]
    values = [df_users_info.iloc[0]["opersite"], pm_tmp_pwd, df_users_info.iloc[1]["opersite"],
              df_users_info.iloc[1]["opersite"]]
    for key, value in zip(keys, values):
        field = chrdriver.chrdriver.find_element(By.ID,key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.chrdriver.find_element(By.ID,"cambio_password").click()
    chrdriver.get(struttura)



def fill_territoriale (chrdriver: webdriver.Chrome, df_config_info: pd.DataFrame,df_users_info: pd.DataFrame):

    chrdriver.chrdriver.find_element(By.ID,"Nuovo").click()
    fillig_dict = dict(
        {"nome": df_users_info.iloc[0]["struttura"], "indirizzo": "CardioCalm", "civico": "23", "cap": "25018", "comune": "Montichiari",
         "provincia": "Brescia", "telefono": "1234567890", "fax": "1234567", "email":df_config_info.iloc[0]["email"],
         "stato": "stato-1", "id_gruppo": df_users_info.iloc[0]["gruppo"], "upload_exam": 1, "data_sospensione": "",

         #OPER DATA

         "nome_operatore_site": "Selenium",
         "cognome_operatore_site": "oper", "telefono_operatore_site": "1234567890", "cellulare_operatore_site": "1234567890",
         "username_operatore_site": df_users_info.iloc[0]["opersite"], "email_operatore_site": df_config_info.iloc[0]["email"],

         #REFERENTE SANITARIO DATA

         "nome_referente_tecnico":"Selenium", "cognome_referente_tecnico":"RefTecnico", "telefono_referente_tecnico": "1234567890",
         "cellulare_referente_tecnico": "1234567890", "email_referente_tecnico": df_config_info.iloc[0]["email"],

         #REFERENTE STRUTTURA

         "stesso_riferimento_tecnico": 1
         })

    for key in fillig_dict.keys():
        if key not in ["upload_exam","stato", "stesso_riferimento_tecnico", "id_gruppo"]:
            field = chrdriver.chrdriver.find_element(By.ID,key)
            field.clear()
            field.send_keys(fillig_dict[key])
        elif key in ["upload_exam", "stesso_riferimento_tecnico"] and fillig_dict[key]==1:
            chrdriver.chrdriver.find_element(By.ID,key).click()
        elif key in ["stato"]:
            chrdriver.chrdriver.find_element(By.ID,fillig_dict[key]).click()
        elif key in ["id_gruppo"]:
            xpath = "//select[@id='id_gruppo']/option[text()='{}']".format(fillig_dict[key])
            chrdriver.chrdriver.find_element(By.ID,xpath).click()
            
    select = Select(chrdriver.chrdriver.find_element(By.ID,"lista_servizi"))
    n_servizi = len(select.options)
    from_element = chrdriver.chrdriver.find_element(By.ID,"//*[@id='lista_servizi']/option[1]")
    to_element = chrdriver.chrdriver.find_element(By.ID,"//*[@id='lista_servizi']/option[{}]".format(n_servizi))
    action = ActionChains(chrdriver)
    action.click_and_hold(from_element).move_to_element(to_element).perform()

    chrdriver.find_element_by_id("Salva").click()

