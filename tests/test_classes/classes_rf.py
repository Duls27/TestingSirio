import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
"""
Classes of Referta Esame test
"""


class exams_rf:

    def __init__(self):
        self.ids = []
        self.types = []
        self.names_surnames = []

    def __iter__(self):
        """
        Iterator of the class

        :return: iterator
        """
        for each in self.__dict__.keys():
            yield self.__getattribute__(each)

