from selenium import webdriver
from selenium.common.exceptions import *


#Funzione che effttua l' accesso ad alla piattaforma
#input: driver, usr, pwd
#return: webdriver con accesso effettuato
def get_access (chrdriver: webdriver.Chrome, usr, pwd):

    try:
        search_field = chrdriver.find_element_by_id("username")
        search_field.clear()
        search_field.send_keys(usr)

        search_field = chrdriver.find_element_by_id("password")
        search_field.clear()
        search_field.send_keys(pwd)
        search_field.submit()
    except NoAlertPresentException:
        chrdriver.switch_to_alert().accept()

    return chrdriver


#Filla un campo normale, ricercando l'id dell' elemento e inserend il valore, non ritorna nulla
def normal_filling (chrdriver: webdriver.Chrome, field, value):
    target = chrdriver.find_element_by_id(field)
    target.clear()
    target.send_keys(value)