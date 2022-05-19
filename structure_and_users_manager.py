import time
import pandas as pd
from selenium import webdriver
import email_manager







def check_structure_existence (chrdriver: webdriver.Chrome ,df_users_info: pd.DataFrame):

    #enter in platform as Admin
    chrdriver=enter_password_double_check(chrdriver, df_users_info["admin"])

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
        print("Da creare!")








def create_structure_test():
    return

#This function try to acces to platform with two different password
#INPUT: chrome driver, dataframe named as last part of login url https:telecardio....../admin or /opersite ... and the rows of table contains user info (one user)
#OUTPUT: chrome driver logged
def enter_password_double_check(chrdriver: webdriver.Chrome, df_usr: pd.DataFrame):
    #create successful url for check if login is done
    successful_url= str(chrdriver.current_url) + df_usr.name

    #fill first time
    search_field = chrdriver.find_element_by_id("username")
    search_field.clear()
    search_field.send_keys(df_usr[0])

    search_field = chrdriver.find_element_by_id("password")
    search_field.clear()
    search_field.send_keys(df_usr[1])
    search_field.submit()
    # chrdriver.switch_to_alert().accept()
    current_url = chrdriver.current_url

    # fill second time, if url mismatch
    if current_url != successful_url:
        search_field = chrdriver.find_element_by_id("username")
        search_field.clear()
        search_field.send_keys(df_usr[0])
        search_field = chrdriver.find_element_by_id("password")
        search_field.clear()
        search_field.send_keys(df_usr[2])
        chrdriver.find_element_by_id("login").click()
        # chrdriver.switch_to_alert().accept()

    return chrdriver