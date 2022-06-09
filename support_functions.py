from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By


#Funzione che effttua l' accesso ad alla piattaforma
#input: driver, usr, pwd
#return: webdriver con accesso effettuato
#This function try to acces to platform with two different password
#INPUT: chrome driver, dataframe named as last part of login url https:telecardio....../admin or /opersite ... and the rows of table contains user info (one user)
#OUTPUT: chrome driver logged
def enter_password_double_check(chrdriver: webdriver.Chrome, df_usr: pd.DataFrame):
    #create successful url for check if login is done
    successful_url= str(chrdriver.current_url) + df_usr.name

    #fill first time
    search_field = chrdriver.find_element(By.ID,"username")
    search_field.clear()
    search_field.send_keys(df_usr[0])

    search_field = chrdriver.find_element(By.ID,"password")
    search_field.clear()
    search_field.send_keys(df_usr[1])
    search_field.submit()
    # chrdriver.switch_to_alert().accept()
    current_url = chrdriver.current_url

    # fill second time, if url mismatch
    if current_url != successful_url:
        search_field = chrdriver.find_element(By.ID,"username")
        search_field.clear()
        search_field.send_keys(df_usr[0])
        search_field = chrdriver.find_element(By.ID,"password")
        search_field.clear()
        search_field.send_keys(df_usr[2])
        chrdriver.find_element(By.ID,"login").click()
        # chrdriver.switch_to_alert().accept()

    return chrdriver


#Filla un campo normale, ricercando l'id dell' elemento e inserend il valore, non ritorna nulla
def normal_filling (chrdriver: webdriver.Chrome, field, value):
    target = chrdriver.find_element(By.ID,field)
    target.clear()
    target.send_keys(value)

