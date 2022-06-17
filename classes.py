import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

class configuration_info:
    def __init__(self,sv: dict):
        self.email = email(usr=sv["email_usr"], pwd=sv["email_pwd"])
        self.path_chrome_driver = str(sv["chrome_driver"])
        self.path_folder_desk= str(sv["path_desktop"]  + sv["name_folder_desktop"])
        self.path_exams=str(sv["path_desktop"]  + sv["name_folder_desktop"] + sv["esami"])
        self.path_diaries=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["diari"])
        self.path_output=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["output"])
        self.path_input=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["input"])

class email:
    def __init__(self, usr, pwd):
        self.usr= usr
        self.pwd= pwd

class users:
    def __init__(self, df_users: pd.DataFrame):
        self.admin=single_user(df_user=df_users.loc[["admin"],:])
        self.pm = single_user(df_user=df_users.loc[["pm"],:])
        self.cardio = single_user(df_user=df_users.loc[["cardio"],:])
        self.opersite = single_user(df_user=df_users.loc[["opersite"],:])
        self.gruppo= structure(df_user=df_users.loc[["gruppo"],:])
        self.struttura = structure(df_user=df_users.loc[["struttura"],:])

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

    def login_admin (self,chrdriver: webdriver.Chrome):
        #create successful url for check if login is done
        successful_url= str(chrdriver.current_url) + self.admin.id
        #fill first time
        search_field = chrdriver.find_element(By.ID,"username")
        search_field.clear()
        search_field.send_keys(self.admin.usr)

        search_field = chrdriver.find_element(By.ID,"password")
        search_field.clear()
        search_field.send_keys(self.admin.pwd1)
        search_field.submit()
        # chrdriver.switch_to_alert().accept()
        current_url = chrdriver.current_url

        # fill second time, if url mismatch
        if current_url != successful_url:
            search_field = chrdriver.find_element(By.ID,"username")
            search_field.clear()
            search_field.send_keys(self.admin.usr)
            search_field = chrdriver.find_element(By.ID,"password")
            search_field.clear()
            search_field.send_keys(self.admin.pwd2)
            chrdriver.find_element(By.ID,"login").click()
            # chrdriver.switch_to_alert().accept()

        return chrdriver

    def login_pm(self, chrdriver: webdriver.Chrome):
        # create successful url for check if login is done
        successful_url = str(chrdriver.current_url) + self.pm.id
        # fill first time
        search_field = chrdriver.find_element(By.ID, "username")
        search_field.clear()
        search_field.send_keys(self.pm.usr)

        search_field = chrdriver.find_element(By.ID, "password")
        search_field.clear()
        search_field.send_keys(self.pm.pwd1)
        search_field.submit()
        # chrdriver.switch_to_alert().accept()
        current_url = chrdriver.current_url

        # fill second time, if url mismatch
        if current_url != successful_url:
            search_field = chrdriver.find_element(By.ID, "username")
            search_field.clear()
            search_field.send_keys(self.pm.usr)
            search_field = chrdriver.find_element(By.ID, "password")
            search_field.clear()
            search_field.send_keys(self.pm.pwd2)
            chrdriver.find_element(By.ID, "login").click()
            # chrdriver.switch_to_alert().accept()

        return chrdriver

    def login_cardio(self, chrdriver: webdriver.Chrome):
        # create successful url for check if login is done
        successful_url = str(chrdriver.current_url) + self.cardio.id
        # fill first time
        search_field = chrdriver.find_element(By.ID, "username")
        search_field.clear()
        search_field.send_keys(self.cardio.usr)

        search_field = chrdriver.find_element(By.ID, "password")
        search_field.clear()
        search_field.send_keys(self.cardio.pwd1)
        search_field.submit()
        # chrdriver.switch_to_alert().accept()
        current_url = chrdriver.current_url

        # fill second time, if url mismatch
        if current_url != successful_url:
            search_field = chrdriver.find_element(By.ID, "username")
            search_field.clear()
            search_field.send_keys(self.cardio.usr)
            search_field = chrdriver.find_element(By.ID, "password")
            search_field.clear()
            search_field.send_keys(self.cardio.pwd2)
            chrdriver.find_element(By.ID, "login").click()
            # chrdriver.switch_to_alert().accept()

        return chrdriver

    def login_opersite(self, chrdriver: webdriver.Chrome):
        # create successful url for check if login is done
        successful_url = str(chrdriver.current_url) + self.opersite.id
        # fill first time
        search_field = chrdriver.find_element(By.ID, "username")
        search_field.clear()
        search_field.send_keys(self.opersite.usr)

        search_field = chrdriver.find_element(By.ID, "password")
        search_field.clear()
        search_field.send_keys(self.opersite.pwd1)
        search_field.submit()
        # chrdriver.switch_to_alert().accept()
        current_url = chrdriver.current_url

        # fill second time, if url mismatch
        if current_url != successful_url:
            search_field = chrdriver.find_element(By.ID, "username")
            search_field.clear()
            search_field.send_keys(self.opersite.usr)
            search_field = chrdriver.find_element(By.ID, "password")
            search_field.clear()
            search_field.send_keys(self.opersite.pwd2)
            chrdriver.find_element(By.ID, "login").click()
            # chrdriver.switch_to_alert().accept()

        return chrdriver

class single_user:
    def __init__(self, df_user: pd.DataFrame):
        self.id=df_user.index.values[0]
        self.usr=str(df_user.iloc[0]["usr"])
        self.pwd1=str(df_user.iloc[0]["pwd1"])
        self.pwd2=str(df_user.iloc[0]["pwd2"])

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class structure:
    def __init__(self, df_user: pd.DataFrame):
        self.id=str(df_user.index.values[0])
        self.name=str(df_user.iloc[0]["usr"])

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class ce_errors:
    def __init__(self):
        self.mancanzaInformazioni=single_ce_error(text="Mancanza di informazioni necessarie per il caricamento dell'esame")
        self.dataEsameNV=single_ce_error(text="Data esame non valida, formato data dd-mm-aaaa")
        self.oraEsameNV=single_ce_error(text="Ora esame non valida")
        self.dataNascitaNV=single_ce_error(text="Data di nascita non valida, formato data dd-mm-aaaa")
        self.pesoNV=single_ce_error(text="Peso non valido")
        self.altezzaNV=single_ce_error(text="Altezza non valida")
        self.new_error=new_error_ce()

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

    def get_all_text(cls):
        return [se.text for se in cls.__iter__()]
    def get_all_exp(cls):
        return [se.exp for se in cls.__iter__()]
    def get_all_eff(cls):
        return [se.eff for se in cls.__iter__()]

    def ce_errors_to_df(self):
        index=[]
        data={"exp":[],
              "eff":[]}
        for err in self.__iter__():
            if err != self.new_error:
                index.append(err.text)
                data["exp"].append(err.exp)
                data["eff"].append(err.eff)
            else:
                for elem in self.new_error.__iter_text__():
                    index.append(elem)
                    data["exp"].append(0)
                    data["eff"].append(2)
        return pd.DataFrame(data=data, index=index)

    def get_flag_result(self):
        df_err= self.ce_errors_to_df()
        df_err["diff"]=df_err["exp"] - df_err["eff"]
        flag=0
        for val in df_err["eff"].values:
            if val == -1 or val == -2:
                flag=1
        return flag

class single_ce_error:
    def __init__(self, text):
        self.text=text
        self.exp=0
        self.eff=0

    def __iter__(self):
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class new_error_ce:
    def __init__(self):
        self.text=[]

    def __iter_text__(self):
        for each in self.text:
            yield each