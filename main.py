import file_manager, test_manager
import os
from selenium import webdriver

#get data from excell file
path_desktop= os.path.normpath(os.path.expanduser("~/Desktop"))
path_bootstrap_excel= path_desktop+"/SirioUI/bootstrap.xlsx"

try:
    df_config =file_manager.get_info_from_excel(path_bootstrap= path_bootstrap_excel, sheet_name='config_info')
except IOError:
    print("Reading Config info excel file ERROR !")

#create directory for screenshots
df_config["path_folder_screenshot"]=path_desktop + "/SirioUI/Screenshot/"
if not os.path.exists(df_config.iloc[0]["path_folder_screenshot"]):
    os.mkdir(df_config.iloc[0]["path_folder_screenshot"])


#open chromebrowser and specific site
try:
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--incognito")
    #private_driver = webdriver.Chrome(df_config.iloc[0]['path_chrome_driver'], options=chrome_options) #opening WebBrowser
    driver=webdriver.Chrome(df_config.iloc[0]['path_chrome_driver'])

except IOError:
    print("Error opening Chrome, check your ChromeWebDriver installation. For package see https://chromedriver.chromium.org/")

driver.get(df_config.iloc[0]['link_piattaforma']) #Open Page to platform

test_manager.test_gateway(chrdriver=driver, path_bootstrap_excel=path_bootstrap_excel, n_row_to_test=0)
