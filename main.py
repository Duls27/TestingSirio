import file_manager, test_manager, structure_and_users_manager
import os, pandas as pd
from selenium import webdriver

#get data from excell file
import structure_and_users_manager

path_desktop= os.path.normpath(os.path.expanduser("~/Desktop"))
path_bootstrap_excel= path_desktop+"/SirioUI/bootstrap.xlsx"

try:
    df_config =file_manager.get_info_from_excel(path_bootstrap= path_bootstrap_excel, sheet_name='config_info')
except IOError:
    print("Reading Config info excel file ERROR !")

#create directory for screenshots
df_config["path_folder_screenshot"] = path_desktop + "/SirioUI/screenshot/"
df_config["path_exams"] = path_desktop + "/SirioUI/esami/"
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

driver.get(df_config.iloc[0]['link_piattaforma']) #Open Page to platform

#########################################################################################################################


#For every value in culumn "link_struttura",in config_info excell bootstrap sheet, check if exist specific users and structure and execute test described in test_manager.test_gateway
for struttura in df_config["link_piattaforma"].tolist():

    structure_and_users_manager.check_structure_existence(chrdriver=driver,path_bootstrap_excel=path_bootstrap_excel)

    #test_manager.test_gateway(chrdriver=driver, path_bootstrap_excel=path_bootstrap_excel, structure=struttura)
