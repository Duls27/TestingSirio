import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
test_classes.py contains basic test_classes regarding users and config_info. 

"""


class configuration_info:

    def __init__(self,sv: dict):
        """
            This class only contain all the information for the configuration of the script.

            :param dictionary that contain all info. Labels of dict must be equal to the label reported here.

            """
        self.email = email(usr=sv["email_usr"], pwd=sv["email_pwd"])
        self.path_chrome_driver = str(sv["chrome_driver"])
        self.path_folder_desk= str(sv["path_desktop"]  + sv["name_folder_desktop"])
        self.path_exams=str(sv["path_desktop"]  + sv["name_folder_desktop"] + sv["esami"])
        self.path_diaries=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["diari"])
        self.path_output=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["output"])
        self.path_input=str(sv["path_desktop"]  + sv["name_folder_desktop"] +sv["input"])

class email:
    def __init__(self, usr: str, pwd: str):
        """
                This class only contain all the information of email type.
                Class only called by the class configuration_info

                :param  usr = string with username, pwd= string with username

                """
        self.usr= usr
        self.pwd= pwd

class users:

    def __init__(self, df_users: pd.DataFrame):
        """
                This class contain all the info of the users of a platform.

                :param  df_users: DataFrame that contains all the informatin about all users, row_names must be equal
                                   to labels reported here.
           """
        self.admin=single_user(df_user=df_users.loc[["admin"],:])
        self.pm = single_user(df_user=df_users.loc[["pm"],:])
        self.cardio = single_user(df_user=df_users.loc[["cardio"],:])
        self.opersite = single_user(df_user=df_users.loc[["opersite"],:])
        self.gruppo= structure(df_user=df_users.loc[["gruppo"],:])
        self.struttura = structure(df_user=df_users.loc[["struttura"],:])

    def __iter__(self):
        """
        ________________________
         Iterator
         _________________________
         Iterate in the object of the class users.

         Output: iterator.
        :return:
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

    def login_admin (self,chrdriver: webdriver.Chrome):

        """
        Function login is use for log a specific user automatically in the platform.
        Login function try to log user at first with pwd1, if pwd1 is not correct function try with pwd2.

        :param chrdriver: driver in the login page of the structure
        :return: chrdriver: logged in structure
        """

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
        """
                Function login is use for log a specific user automatically in the platform
                Login function try to log user at first with pwd1, if pwd1 is not correct function try with pwd2.

                :param chrdriver: driver in the login page of the structure
                :return: chrdriver: logged in structure
                """
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
        """
                Function login is use for log a specific user automatically in the platform
                Login function try to log user at first with pwd1, if pwd1 is not correct function try with pwd2.

                :param chrdriver: driver in the login page of the structure
                :return: chrdriver: logged in structure
                """
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
        """
                Function login is use for log a specific user automatically in the platform
                Login function try to log user at first with pwd1, if pwd1 is not correct function try with pwd2

                :param chrdriver: driver in the login page of the structure
                :return: chrdriver: logged in structure
                """
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
        """
        Class that contains the information of a specific user: username, password1, password2 (other possible password)

        :param df_user: single row DataFrame, with row_names setted as label that contains info of specific user
        """
        self.id=df_user.index.values[0]
        self.usr=str(df_user.iloc[0]["usr"])
        self.pwd1=str(df_user.iloc[0]["pwd1"])
        self.pwd2=str(df_user.iloc[0]["pwd2"])

    def __iter__(self):
        """
        Iteratore of the class

        :return: iterator
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class structure:

    def __init__(self, df_user: pd.DataFrame):
        """
        Instantiate the object structure, that contain only name of the structure and id, id ist the last part of logged url.
        Ex. https://web.cardiocalm.com/productionTelemedico/opersite, id = opersite

        :param df_user: one row Dataframe, with row_names setted as label of specific structure
        """
        self.id=str(df_user.index.values[0])
        self.name=str(df_user.iloc[0]["usr"])

    def __iter__(self):
        """
        Iterator of class structure

        :return: iterator
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)


import _io, sys

class Wrapper:
    def __init__(self, stdout: _io.TextIOWrapper, target_log_file: _io.TextIOWrapper):
        self.target_log_file = target_log_file
        self.stdout = stdout

    def write(self, o):
        self.target_log_file.write(o)
        self.stdout.write(o)

    def flush(self):
        self.target_log_file.flush()
        self.stdout.flush()
