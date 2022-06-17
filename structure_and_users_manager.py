from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
import email_manager, classes

def check_structure_existence (chrdriver: webdriver.Chrome, config_info: classes.configuration_info , users: classes.users, platform):

        #enter in platform as Admin
        chrdriver=users.login_admin(chrdriver=chrdriver)

        ###########################################       GRUPPO       #####################################################
        # check if exist gruppo
        chrdriver.find_element_by_link_text("Configura Strutture").click()
        chrdriver.find_element_by_link_text("Gruppi Strutture Territoriali").click()
        groups_name = chrdriver.find_element(By.ID,"id_gruppo_centri_raccolta_ecg").find_elements(By.TAG_NAME,"option")
        flag_create_group = 1
        for group in groups_name:
            if users.gruppo.name in group.text:
                flag_create_group = 0
                break
        if flag_create_group == 1:
            create_gruppo(chrdriver=chrdriver, users=users)
            chrdriver.get(platform)
            chrdriver=users.login_admin()

        #######################################       PROJECT MANAJER       ################################################
        # check if exist refertatore

        chrdriver.find_element(By.LINK_TEXT,"Gestione Utenti").click()
        chrdriver.find_element(By.LINK_TEXT,"Project Manager").click()
        pms_name = chrdriver.find_element(By.ID,"id_utente").find_elements_by_tag_name("option")
        flag_create_pm = 1
        for pm in pms_name:
            if users.pm.usr in pm.text:
                flag_create_pm = 0
                break
        if flag_create_pm == 1:
            create_pm(chrdriver=chrdriver,config_info=config_info, users=users, platform=platform)
            chrdriver.get(platform)
            chrdriver=users.login_admin(chrdriver=chrdriver)

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
            if str(users.struttura.name) in territoriale.text:
                flag_create_opersite = 0
                break

        if flag_create_opersite == 1:
            create_territoriale(chrdriver=chrdriver, users=users, config_info=config_info, platform=platform)
            chrdriver.get(platform)
            chrdriver=users.login_admin(chrdriver=chrdriver)

       #####################################       CARDIO       ######################################################
        # check if exist refertatore
        chrdriver.find_element_by_link_text("Gestione Utenti").click()
        chrdriver.find_element_by_link_text("Refertatori").click()
        cardios_name = chrdriver.find_element_by_id("id_utente").find_elements_by_tag_name("option")

        flag_create_cardio = 1
        for cardio in cardios_name:
            if users.cardio.usr in cardio.text:
                flag_create_cardio = 0
                break
        if flag_create_cardio == 1:
            create_cardio(chrdriver=chrdriver, users=users, config_info=config_info, platform=platform)
            chrdriver.get(platform)


################################## FUNCTIONS FOR CREATION OF USERS #################################################
####################################### PM FUNCTIONS ###########################################################
def create_pm (chrdriver: webdriver.Chrome , config_info: classes.configuration_info, users: classes.users, platform):

    email_manager.delete_all_emails(username= config_info.email.usr, password= config_info.email.pwd)
    fill_pm( chrdriver,config_info=config_info, users=users)
    email_manager.await_receipt_of_email(username= config_info.email.usr, password= config_info.email.pwd)
    mails = email_manager.get_emails(username= config_info.email.usr, password= config_info.email.pwd)
    pm_tmp_pwd=email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(platform)
    #do_first acces
    keys=["username","password","nuova_password", "ridigita_nuova_password"]
    values=[users.pm.usr, pm_tmp_pwd ,users.pm.pwd1,users.pm.pwd1]
    for key,value in zip(keys, values):
        field = chrdriver.find_element(By.ID,key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element(By.ID,"cambio_password").click()

def fill_pm (chrdriver: webdriver.Chrome, config_info: classes.configuration_info,users: classes.users):
    chrdriver.find_element(By.XPATH,'//input[@value="Nuovo Project Manager"]').click()
    fillig_dict=dict({"nome": "Selenium" ,"cognome": "pm","datadinascita": "20-11-1998","luogodinascita": "CardioCalm","indirizzo_email": config_info.email.usr  ,"numero_cellulare": "1234567890", "username": users.pm.usr})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element_by_id(key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.find_element(By.ID,"dati_sensibili").click()
    chrdriver.find_element(By.ID,"autenticazione-0").click()  #sirio internal user

    gruppo = chrdriver.find_element(By.XPATH,"//*[@id='gruppo_centri_raccolta_ecg']/option[text()= '{}']".format(users.gruppo.name))
    gruppo.click()

    chrdriver.find_element(By.ID,"Salva").click()  # sirio

########################################## CARDIO FUNCTIONS ##########################################################

def create_cardio(chrdriver: webdriver.Chrome,config_info: classes.configuration_info,users: classes.users, platform):

    email_manager.delete_all_emails(username= config_info.email.usr, password= config_info.email.pwd)
    fill_cardio(chrdriver, config_info=config_info, users=users)
    email_manager.await_receipt_of_email(username= config_info.email.usr, password= config_info.email.pwd)

    mails = email_manager.get_emails(username= config_info.email.usr, password= config_info.email.pwd)
    pm_tmp_pwd = email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(platform)
    # do_first acces
    keys = ["username", "password", "nuova_password", "ridigita_nuova_password"]
    values = [users.cardio.usr, pm_tmp_pwd, users.cardio.pwd1, users.cardio.pwd1]
    for key, value in zip(keys, values):
        field = chrdriver.find_element(By.ID,key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element(By.ID,"cambio_password").click()

def fill_cardio (chrdriver: webdriver.Chrome,config_info: classes.configuration_info,users: classes.users):

    chrdriver.find_element(By.XPATH,'//input[@value="Nuovo Cardiologo"]').click()
    fillig_dict = dict(
        {"nome": "Selenium", "cognome": "cardio", "datadinascita": "20-11-1998", "luogodinascita": "CardioCalm",
         "indirizzo_email": config_info.email.usr, "numero_cellulare": "1234567890",
         "username": users.cardio.usr, "n_iscriz_ordine": "1234"})

    # filliig New Administrator
    for key in fillig_dict.keys():
        field = chrdriver.find_element(By.ID,key)
        field.clear()
        field.send_keys(fillig_dict[key])

    chrdriver.find_element(By.ID,"delete_firma").click()
    chrdriver.find_element(By.ID,"supervisore").click()
    chrdriver.find_element(By.ID,"autenticazione-0").click()  # sirio internal user

    gruppo = chrdriver.find_element(By.XPATH,"//*[@id='gruppo_centri_raccolta_ecg']/option[text()= '{}']".format(users.gruppo.name))
    gruppo.click()

    select = Select(chrdriver.find_element(By.ID,"tipi_esame"))
    n_servizi = len(select.options)
    from_element = chrdriver.find_element(By.XPATH,"//*[@id='tipi_esame']/option[1]")
    to_element = chrdriver.find_element(By.XPATH,"//*[@id='tipi_esame']/option[{}]".format(n_servizi))
    action = ActionChains(chrdriver)
    action.click_and_hold(from_element).move_to_element(to_element).perform()


    chrdriver.find_element(By.ID,"Salva").click()  # sirio

########################################### GRUPPO FUNCTIONS ########################################################

def create_gruppo (chrdriver: webdriver.Chrome, users: classes.users):

    chrdriver.find_element(By.ID,"Nuovo").click()
    name=chrdriver.find_element(By.ID,"nome")
    name.send_keys(users.gruppo.name)
    chrdriver.find_element(By.ID,"Salva").click()

####################################### TERRITORIALE E OPER FUNCTIONS ##############################################

def create_territoriale (chrdriver: webdriver.Chrome, config_info: classes.configuration_info,users: classes.users, platform):

    email_manager.delete_all_emails(username= config_info.email.usr, password= config_info.email.pwd)
    fill_territoriale(chrdriver, config_info=config_info, users=users)
    email_manager.await_receipt_of_email(username= config_info.email.usr, password= config_info.email.pwd)
    mails = email_manager.get_emails(username= config_info.email.usr, password= config_info.email.pwd)
    pm_tmp_pwd = email_manager.get_tmp_pwd_from_emails(mails)

    chrdriver.get(platform)
    # do_first acces
    keys = ["username", "password", "nuova_password", "ridigita_nuova_password"]
    values = [users.opersite.usr, pm_tmp_pwd, users.opersite.pwd1,users.opersite.pwd1]
    for key, value in zip(keys, values):
        field = chrdriver.find_element(By.ID,key)
        field.send_keys(value)
        if key == "password":
            field.submit()

    chrdriver.find_element(By.ID,"cambio_password").click()
    chrdriver.get(platform)

def fill_territoriale (chrdriver: webdriver.Chrome, config_info: classes.configuration_info,users: classes.users):

    chrdriver.find_element(By.ID,"Nuovo").click()
    fillig_dict = dict(
        {"nome": users.struttura.name, "indirizzo": "CardioCalm", "civico": "23", "cap": "25018", "comune": "Montichiari",
         "provincia": "Brescia", "telefono": "1234567890", "fax": "1234567", "email":config_info.email.usr,
         "stato": "stato-1", "id_gruppo": users.gruppo.name, "upload_exam": 1, "data_sospensione": "",

         #OPER DATA

         "nome_operatore_site": "Selenium",
         "cognome_operatore_site": "oper", "telefono_operatore_site": "1234567890", "cellulare_operatore_site": "1234567890",
         "username_operatore_site": users.opersite.usr, "email_operatore_site": config_info.email.usr,

         #REFERENTE SANITARIO DATA

         "nome_referente_tecnico":"Selenium", "cognome_referente_tecnico":"RefTecnico", "telefono_referente_tecnico": "1234567890",
         "cellulare_referente_tecnico": "1234567890", "email_referente_tecnico": config_info.email.usr,

         #REFERENTE STRUTTURA

         "stesso_riferimento_tecnico": 1
         })

    for key in fillig_dict.keys():
        if key not in ["upload_exam","stato", "stesso_riferimento_tecnico", "id_gruppo"]:
            field = chrdriver.find_element(By.ID,key)
            field.clear()
            field.send_keys(fillig_dict[key])
        elif key in ["upload_exam", "stesso_riferimento_tecnico"] and fillig_dict[key]==1:
            chrdriver.find_element(By.ID,key).click()
        elif key in ["stato"]:
            chrdriver.find_element(By.ID,fillig_dict[key]).click()
        elif key in ["id_gruppo"]:
            xpath = "//select[@id='id_gruppo']/option[text()='{}']".format(fillig_dict[key])
            chrdriver.find_element(By.XPATH,xpath).click()
            
    select = Select(chrdriver.find_element(By.ID,"lista_servizi"))
    n_servizi = len(select.options)
    from_element = chrdriver.find_element(By.XPATH,"//*[@id='lista_servizi']/option[1]")
    to_element = chrdriver.find_element(By.XPATH,"//*[@id='lista_servizi']/option[{}]".format(n_servizi))
    action = ActionChains(chrdriver)
    action.click_and_hold(from_element).move_to_element(to_element).perform()

    chrdriver.find_element_by_id("Salva").click()

