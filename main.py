import  structure_and_users_manager, classes, test_manager
import os, pandas as pd
from selenium import webdriver

############################################  INFORMATION REQUIRED  ####################################################

settable_values = {"email_usr": "testing@amps-llc.com",
                   "email_pwd": "aXmm149&",
                   "name_folder_desktop": "/SeleniumTest",
                   "diari": "/diari",
                   "esami": "/esami",
                   "screenshot": "/screenshot",
                   "input": "/bootstrap.xlsx",
                   "output": "/results.xlxs",
                   "chrome_driver": "C:\Program Files\Google\Chrome\Application\chromedriver.exe",
                   "path_desktop": os.path.normpath(os.path.expanduser("~/Desktop"))}

########################################################################################################################

#assign variables for configuration to specific class
config_info=classes.configuration_info(sv=settable_values)

############################################  OPENING CHROME DRIVER  ##################################################

try:
    #chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--incognito")
    #private_driver = webdriver.Chrome(df_config.iloc[0]['path_chrome_driver'], options=chrome_options) #opening WebBrowser
    driver=webdriver.Chrome(config_info.path_chrome_driver)

except IOError:
    print("Error opening Chrome, check your ChromeWebDriver installation. For package see https://chromedriver.chromium.org/")

#########################################################################################################################

lista_test = pd.read_excel(config_info.path_input, sheet_name='lista_test', index_col="link_piattaforma")
platforms=lista_test.index.values
df_users = pd.read_excel(config_info.path_input, sheet_name='users_info', index_col="row_names")
#Set class of users_info
users=classes.users(df_users=df_users)


for platform in platforms:
    # Create folder for result of specific platform
    name_platform = platform.split(sep="/")[3]
    folder_plat = str(config_info.path_folder_desk + "/" + name_platform)
    if not os.path.isdir(folder_plat):
        os.mkdir(folder_plat)

    print(f"\n*******************************************************************************"
          f"\n Controlling if users exist for: {name_platform}\n")

    #driver.get(platform)  # Open Page to platform
    #structure_and_users_manager.check_structure_existence(chrdriver=driver,config_info= config_info, users=users,platform=platform)

    print(f"\n*******************************************************************************"
          f"\n Starting with test of {name_platform}\n")

    driver.get(platform)
    #chunk lista test only of one platform
    lista_test_platofrom= lista_test.loc[platform]
    test_manager.test_gateway(chrdriver=driver, config_info=config_info, lista_test_platofrom=lista_test_platofrom, users= users, folder_platform=folder_plat)

print("Well done, but this not means that all goes like you thinked!")

driver.close()
exit()