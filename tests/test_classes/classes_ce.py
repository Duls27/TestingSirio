import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
"""
Classes of Carica Esame test
"""

class errors:

    def __init__(self):
        """
        Instantiate the object ce_errors, this are specific errors of Carica Esame test. The errors reported here are
         the only once that the script if is necessary recognize as "Expected errors". The functin for calculate if are
         "expected errors is in test_carica_esame -> set_expected_error".
         If you wan to add other errors create here the self.error obj and that handle his capture in set_expected_errors

         Every object is a single_ce_error object, only require that you insert manually text error.
        """

        self.mancanzaInformazioni=single_error(text="Mancanza di informazioni necessarie per il caricamento dell'esame")
        self.dataEsameNV=single_error(text="Data esame non valida, formato data dd-mm-aaaa")
        self.oraEsameNV=single_error(text="Ora esame non valida")
        self.dataNascitaNV=single_error(text="Data di nascita non valida, formato data dd-mm-aaaa")
        self.pesoNV=single_error(text="Peso non valido")
        self.altezzaNV=single_error(text="Altezza non valida")
        self.esameDoppio=single_error(text="Esame inviato ma bloccato, esiste un altro esame associato allo stesso utente e registrato nello stesso istante")
        self.new_error=new_error()

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

    def get_flagRes_flagSend(self):
        """
        This function return two flags:
        flagRes: 0 if there are no errors to report to the user, 1 if there are errors, thi is eveluated doing err_expected - err_effective.
                - 2 is not error, cause is expected but exam is sended
        flagSend: 1 if the exam is sended, 0 if exam is NOT sended, -1 if exam is BLOCKED. Evaluate only effective errors,
                in case of BLOCKED search if exp-eff is equal to -2, cause error related to duplicates is the only one that have exp err = -1, so re is -2.
        :return: two bynaries flags
        """

        df_err= self.ce_errors_to_df()
        df_err["diff"]=df_err["exp"] - df_err["eff"]
        flaRes=0
        flaSend=1
        #check if exam is sended or not
        for val in df_err["eff"].values:
            if val == 1:
                flaSend = 0
        #evaluate if in report file insert that there is a problem
        for val in df_err["diff"].values:
            if val == -1:
                flaRes=1
            if val == -2: #Exam is sended, but blocked set flag to -1
                flaSend=-1

        return flaRes, flaSend

class single_error:

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

class new_error:
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
