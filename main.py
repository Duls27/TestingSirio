import file_manager, test_manager, structure_and_users_manager
import os, pandas as pd
from selenium import webdriver

name_folder_on_desktop="/SirioUI"
#get data from excell file
import structure_and_users_manager

path_desktop= os.path.normpath(os.path.expanduser("~/Desktop"))
path_bootstrap_excel= path_desktop+ name_folder_on_desktop +"/bootstrap.xlsx"

try:
    df_config =file_manager.get_info_from_excel(path_bootstrap= path_bootstrap_excel, sheet_name='config_info')
except IOError:
    print("Reading Config info excel file ERROR !")

#create directories path if are not set, if not set paths have to be as required
if df_config['path_folder_screenshot'].isnull().values.any():
    df_config["path_folder_screenshot"] = path_desktop + name_folder_on_desktop +"/screenshot"
if df_config['path_exams'].isnull().values.any():
    df_config["path_exams"] = path_desktop + name_folder_on_desktop +"/esami"
if df_config['path_diaries'].isnull().values.any():
    df_config["path_diaries"]= path_desktop + name_folder_on_desktop +"/diari"
if not os.path.exists(df_config.iloc[0]["path_folder_screenshot"]):
    os.mkdir(df_config.iloc[0]["path_folder_screenshot"])
with pd.ExcelWriter(path_bootstrap_excel,mode='a', if_sheet_exists="overlay") as writer:
    df_config.to_excel(writer, sheet_name='config_info', index= False)

############################################################################################################################

#open chromebrowser and specific site
try:
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--incognito")
    #private_driver = webdriver.Chrome(df_config.iloc[0]['path_chrome_driver'], options=chrome_options) #opening WebBrowser
    driver=webdriver.Chrome(df_config.iloc[0]['path_chrome_driver'])

except IOError:
    print("Error opening Chrome, check your ChromeWebDriver installation. For package see https://chromedriver.chromium.org/")

#########################################################################################################################

#For every value in culumn "link_struttura",in config_info excell bootstrap sheet, check if exist specific users and structure and execute test described in test_manager.test_gateway
for struttura in df_config["link_piattaforma"].tolist():

    driver.get(struttura)  # Open Page to platform
    structure_and_users_manager.check_structure_existence(chrdriver=driver,path_bootstrap_excel=path_bootstrap_excel, struttura=struttura)

for struttura, index in zip(df_config["link_piattaforma"].tolist(), range(0,len(df_config["link_piattaforma"].tolist()))):
    driver.get(struttura)  # Open Page to platform
    test_manager.test_gateway(chrdriver=driver, path_bootstrap_excel=path_bootstrap_excel, platform_index=index)

print("Well done, but this not means that all goes like you thinked!")

driver.close()
exit()