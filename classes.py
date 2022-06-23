import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

"""
classes.py contains all the class for run all the code. 
Contain general classes and classes related to test.
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

"""
Classes of Carica Esame test
"""

class ce_errors:

    def __init__(self):
        """
        Instantiate the object ce_errors, this are specific errors of Carica Esame test. The errors reported here are
         the only once that the script if is necessary recognize as "Expected errors". The functin for calculate if are
         "expected errors is in test_carica_esame -> set_expected_error".
         If you wan to add other errors create here the self.error obj and that handle his capture in set_expected_errors

         Every object is a single_ce_error object, only require that you insert manually text error.
        """

        self.mancanzaInformazioni=single_ce_error(text="Mancanza di informazioni necessarie per il caricamento dell'esame")
        self.dataEsameNV=single_ce_error(text="Data esame non valida, formato data dd-mm-aaaa")
        self.oraEsameNV=single_ce_error(text="Ora esame non valida")
        self.dataNascitaNV=single_ce_error(text="Data di nascita non valida, formato data dd-mm-aaaa")
        self.pesoNV=single_ce_error(text="Peso non valido")
        self.altezzaNV=single_ce_error(text="Altezza non valida")
        self.new_error=new_error_ce()

    def __iter__(self):
        """
        Iterator of the class

        :return: iterator
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

    def get_all_text(cls):
        """
        This function return all text of the errors in class ce_errors
        :return: list errorrs
        """
        return [se.text for se in cls.__iter__()]
    def get_all_exp(cls):
        """
                This function return all exp of the errors in class ce_errors
                :return: list expected
                """
        return [se.exp for se in cls.__iter__()]
    def get_all_eff(cls):
        """
                        This function return all exp of the effective in class ce_errors
                        :return: list effective
                        """
        return [se.eff for se in cls.__iter__()]

    def ce_errors_to_df(self):
        """
        This function tranform the class ce_errors in a Dataframe with text_errors as row_names, and columns are exp and eff errors

        :return: DataFrame
        """
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
        """
        This function evaluate if there are new_errors detected of if there are unexpected errors.
        Simply made exp errors - effective errors and evaluate the result

        :return: flag == 1 if there are new/unexpected errors, 0 otherwise
        """
        df_err= self.ce_errors_to_df()
        df_err["diff"]=df_err["exp"] - df_err["eff"]
        flag=0
        for val in df_err["eff"].values:
            if val == -1 or val == -2:
                flag=1
        return flag

class single_ce_error:

    """
    Made for ce_errors class
    This class is made for a single error, contain his text, and instantiate a flag for the eff and expected errors
    """
    def __init__(self, text):
        self.text=text
        self.exp=0
        self.eff=0

    def __iter__(self):
        """
        Iterator of the class
        :return: iterator
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

class new_error_ce:
    """
    Made for ce_errors class
    This class is equal to single error, but new_error_ce has no exp and eff flag cause it's a new error
    """
    def __init__(self):
        self.text=[]

    def __iter_text__(self):
        """
        Iterator of the class
        :return: iterator
        """
        for each in self.text:
            yield each