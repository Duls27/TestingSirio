import time, pandas as pd, datetime, re, os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import classes


def report_more_exams (chrdriver: webdriver.Chrome, users: classes.users):

    users.login_admin(chrdriver=chrdriver)
    print()
