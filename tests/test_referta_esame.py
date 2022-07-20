import string
import time, sys
from pathlib import Path
from string import digits
import numpy as np
import pandas as pd, os
from selenium import webdriver
from datetime import date
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from datetime import datetime
import classes, file_manager



def report_more_exams (chrdriver: webdriver.Chrome, users: classes.users, config_info: classes.configuration_info, sended_exam: list, path_screen:str):

    df_referta_esame = pd.read_excel(config_info.path_input, sheet_name="referta_esame")
    url_platform=chrdriver.current_url
    #Check that exams are arrived, viewing from ADMIN
    df_referta_esame["stato"]=label_encoder(encode_param={'Refertabile': 1, "0": 0, 'Bloccato': -1},to_encode=sended_exam)
    df_exams_status = get_all_table_exams_POV_admin(chrdriver=chrdriver, users=users, dir_exams=config_info.path_exams)
    n_sende_exam=np.count_nonzero(a=sended_exam) #0 aren't sended
    # drop elemnt that are not sended (in sended_list=0), control if other exams are arrived
    df_arrived_exams=pd.merge(df_referta_esame, df_exams_status, on=["stato", "codice_fiscale"], how="inner")
    if n_sende_exam != df_arrived_exams.shape[0]:
        print("ERROR...  Number of sended exam is different from Admin POV")
        return 1
    """
    POP elemnt that are BLOCKED, in case of a specific test, remove POP
    """
    ids=df_arrived_exams[df_arrived_exams['stato']=="Bloccato"].index.values.tolist()
    if len(ids) != 0:
        print(f"\n\tExam/s with index: {ids} is/are correctly set to BLOCKED!")
    df_arrived_exams.drop(ids, inplace=True)
    """
    Insert data of carica esame and associate to df_arrived exams
    """
    df_ce = pd.read_excel(config_info.path_input, sheet_name="carica_esame").drop_duplicates(subset="inp_cf_paziente")
    df_ex_to_report=pd.merge(df_arrived_exams, df_ce, left_on="codice_fiscale", right_on="inp_cf_paziente", how='inner').set_index('nome_cognome')

    chrdriver.get(url_platform)
    #Enter as Cardio for report exams
    users.login_cardio(chrdriver=chrdriver)
    #view all exam in table
    tutti = chrdriver.find_element(By.XPATH, "// *[ @ id = 'sel_sla'] / option[1]")
    actionChains = ActionChains(chrdriver)
    actionChains.double_click(tutti).perform()
    n_exam_to_report=df_ex_to_report.index.shape[0]

    #REPORT EXAMS
    for _ in range(n_exam_to_report):
        time.sleep(3)
        # return all element in table
        #at each iteration cause the platform is updated evry time
        elements_in_table = chrdriver.find_elements(By.XPATH, "//*[@id='idTbodyEcgdarefertare']/*")
        for exam in elements_in_table:

            tds=exam.find_elements(By.TAG_NAME, "td")
            name=tds[5].text
            str=tds[7].text
            if name in df_ex_to_report.index and str == users.struttura.name:
                print(f"\n Reporting {name}\n")
                type_exam=df_ex_to_report.loc[name]["file_exam"]
                actionChains = ActionChains(chrdriver)
                if type_exam=="pdf" or type_exam=="PDF" :
                    actionChains.double_click(exam).perform()
                    one_row_df = df_ex_to_report.loc[name]
                    report_pdf_exam(chrdriver=chrdriver, df_esame=one_row_df, path_screen=path_screen, path_report=file_manager.get_specific_file_from_folder("pdf", config_info.path_exams))
                    break
                else:
                    actionChains.double_click(exam).perform()
                    one_row_df=df_ex_to_report.loc[name]
                    flag_dwn, flag_dati=report_generic_exam(chrdriver=chrdriver, df_esame=one_row_df, path_screen=path_screen, path_report=file_manager.get_specific_file_from_folder("pdf", config_info.path_exams))
                    break

        #if control status for ech exam by admin, write code here (use another chdriver)
'''
def report_borsam_exam(chrdriver: webdriver.Chrome, df_esame: pd.DataFrame, path_screen: str, path_report: str):
    flag_dati = check_dati(chrdriver=chrdriver, df_esame=df_esame, path_screen=path_screen)
    downloads_path = str(Path.home() / "Downloads")
    chrdriver.find_element(By.XPATH, "//*[@id='divIdDownloadEsame']/div/div[2]/div[1]/div/button").click()
    flag_download = download_wait(downloads_path, df_esame)
    #open borsam in CER-S
    chrdriver.find_element(By.XPATH, "//*[@id='divIdDownloadEsame']/div/div[2]/div[1]/div[2]/button").click()
'''
def report_pdf_exam(chrdriver: webdriver.Chrome, df_esame: pd.DataFrame, path_screen: str, path_report: str):
    flag_dati = check_dati(chrdriver=chrdriver, df_esame=df_esame, path_screen=path_screen, is_pdf= True)
    interpretazione=chrdriver.find_element(By.ID, 'interpretazioni_standard')
    for opt in interpretazione.find_elements(By.TAG_NAME, "option"):
        interpretazione.click()
        opt.click()
    chrdriver.find_element(By.ID, "crea_referto").click()
    print("")

def report_generic_exam(chrdriver: webdriver.Chrome, df_esame: pd.DataFrame, path_screen: str, path_report: str):
    flag_dati=check_dati(chrdriver=chrdriver, df_esame=df_esame, path_screen=path_screen, is_pdf=False)
    downloads_path = str(Path.home() / "Downloads")
    chrdriver.find_element(By.XPATH, "//*[@id='divIdDownloadEsame']/div/div[2]/div[1]/div/button").click()
    flag_download=download_wait(downloads_path, df_esame)
    report_file_input=chrdriver.find_element(By.ID, "referto")
    report_file_input.send_keys(path_report)
    chrdriver.find_element(By.ID, "Carica").click()
    chrdriver.find_element(By.XPATH, "/html/body/div[4]/div/div/div/div[2]/div[3]/form/button").click()

    return  flag_download, flag_dati

def check_dati (chrdriver: webdriver.Chrome, df_esame: pd.DataFrame, path_screen:str, is_pdf: bool):
    flag_res=0
    lbl_flag=[]
    table_dati_sogg=chrdriver.find_element(By.XPATH, "//*[@id='divIdDatiSoggetto']/div/div[2]/table")
    elements=table_dati_sogg.find_elements(By.TAG_NAME, "tr")
    for elem in elements:
        lbl=elem.find_element(By.TAG_NAME, "th").text
        val=elem.find_element(By.TAG_NAME, "td").text
        if lbl == "Nome:":
            if  pd.notnull(df_esame.loc["inp_nome_paziente"]) or  pd.notnull(df_esame.loc["inp_cognome_paziente"]):
                if val != str(df_esame.loc["inp_nome_paziente"] + " " + df_esame.loc["inp_cognome_paziente"]):flag_res=1
            else:
                if val != "":
                    flag_res = 1
                    lbl_flag.append(lbl)
        elif lbl == "C.F.:":
            if val != df_esame.loc["inp_cf_paziente"]:
                flag_res = 1
                lbl_flag.append(lbl)
        elif lbl == "Data di N.:":
            if pd.notnull(df_esame.loc["inp_data_di_nascita"]):
                if val != df_esame.loc["inp_data_di_nascita"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
            else:
                if val != "":
                    flag_res = 1
                    lbl_flag.append(lbl)
        elif lbl == "Razza:":
            if pd.notnull(df_esame.loc["inp_data_di_nascita"]):
                if val != df_esame.loc["inp_sel_razza"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
        elif lbl == "Sesso:":
            if pd.notnull(df_esame.loc["inp_data_di_nascita"]):
                if val != df_esame.loc["inp_sel_sesso"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
    if is_pdf:
        #first table
        table_1=chrdriver.find_element(By.XPATH, "/html/body/div[4]/div/div/div[3]/div/div[2]/table/tbody/tr[1]/td[1]/table")
        elements = table_1.find_elements(By.TAG_NAME, "tr")
        for index,elem in enumerate(elements):
            lbl = elem.find_element(By.TAG_NAME, "th").text
            val = elem.find_element(By.TAG_NAME, "td").text
            if lbl == "Eta`:":
                if pd.notnull(df_esame.loc["inp_data_di_nascita"]):
                    if val != str(age(birthdate=df_esame.loc["inp_data_di_nascita"])):
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res=1
                    lbl_flag.append(lbl)
            elif lbl == "Altezza:":
                val=''.join(c for c in val if c in digits)  # remove cm
                if pd.notnull(df_esame.loc["inp_altezza_paziente"]):
                    if val != str(df_esame.loc["inp_altezza_paziente"]):
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res=1
                    lbl_flag.append(lbl)
            elif lbl == "Peso:":
                val = ''.join(c for c in val if c in digits)  # remove kg
                if pd.notnull(df_esame.loc["inp_peso_paziente"]):
                    if val != str(df_esame.loc["inp_peso_paziente"]):
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)

        # table2
        table_2 = chrdriver.find_element(By.XPATH,
                                         "/html/body/div[4]/div/div/div[3]/div/div[2]/table/tbody/tr[1]/td[2]/table")
        elements = table_2.find_elements(By.TAG_NAME, "tr")
        for elem in elements:
            lbl = elem.find_element(By.TAG_NAME, "th").text
            val = elem.find_element(By.TAG_NAME, "td").text
            if lbl == "Motivo:":
                if val != df_esame.loc["inp_motivo_esame"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Terapia:":
                if pd.notnull(df_esame.loc["inp_terapia"]):
                    if val != df_esame.loc["inp_terapia"]:
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Pacemaker:":
                if df_esame.loc["inp_check_pacemaker"] == 1:
                    if val != "SI-":
                        flag_res = 1
                        lbl_flag.append(lbl)
                else:
                    if val != "NO-":
                        flag_res = 1
                        lbl_flag.append(lbl)

        #table3
        table_3 = chrdriver.find_element(By.XPATH,"/ html / body / div[4] / div / div / div[3] / div / div[2] / table / tbody / tr[2] / td / table")
        elements = table_3.find_elements(By.TAG_NAME, "tr")
        for elem in elements:
            lbl = elem.find_element(By.TAG_NAME, "th").text
            val = elem.find_element(By.TAG_NAME, "td").text
            if lbl == "Note:":
                if  pd.notnull(df_esame.loc["inp_note"]):
                    if val != df_esame.loc["inp_note"]:
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)
        if flag_res==1:
            chrdriver.save_screenshot(filename=path_screen + "/error_in_dati.png")
            print(f"\tAll exam data are     NOT     correctly reported, check label {lbl_flag}")
        else:
            print("\tAll exam data are correctly reported")

    else:
        table_dati_esame = chrdriver.find_element(By.XPATH, "//*[@id='datiesame']/div/div[3]/div/div[2]/table")
        elements = table_dati_esame.find_elements(By.TAG_NAME, "tr")
        for index,elem in enumerate(elements):
            lbl = elem.find_element(By.TAG_NAME, "th").text
            val = elem.find_element(By.TAG_NAME, "td").text
            if index == 0 or index == 7:
                continue
            if lbl == "Altezza:":
                val = ''.join(c for c in val if c in digits)  # remove cm
                if pd.notnull(df_esame.loc["inp_altezza_paziente"]):
                    if val !=str(df_esame.loc["inp_altezza_paziente"]):
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Peso:":
                val = ''.join(c for c in val if c in digits)  # remove kg
                if pd.notnull(df_esame.loc["inp_peso_paziente"]):
                    if val != str(df_esame.loc["inp_peso_paziente"]):
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Motivo:":
                if val != df_esame.loc["inp_motivo_esame"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Terapia:":
                if val != df_esame.loc["inp_terapia"]:
                    flag_res = 1
                    lbl_flag.append(lbl)
            elif lbl == "Pacemaker:":
                if "SI" in val:
                    if int(df_esame.loc["inp_check_pacemaker"]) != 1:
                        flag_res = 1
                        lbl_flag.append(lbl)
                else:
                    if pd.notnull(df_esame.loc["inp_check_pacemaker"]):
                        flag_res = 1
                        lbl_flag.append(lbl)
            elif lbl == "Note:":
                if pd.notnull(df_esame.loc["inp_note"]):
                    if val != df_esame.loc["inp_note"]:
                        flag_res = 1
                        lbl_flag.append(lbl)
                elif len(val):
                    flag_res = 1
                    lbl_flag.append(lbl)
        if flag_res==1:
            chrdriver.save_screenshot(filename=path_screen + "/error_in_dati.png")
            print(f"\tAll exam data are     NOT     correctly reported, check label {lbl_flag}")
        else:
            print("\tAll exam data are correctly reported")

    return flag_res

def get_all_table_exams_POV_admin(chrdriver: webdriver.Chrome, users: classes.users, dir_exams: str):
    """
    Log as amdin and goes to the "Modifica stato esame" page, from this page select the exams of structure in users class,
    insert dates, from: oldest date between files in exam folder, to: today date.
    Return a datframe equal to the table in the page, only if all exams are arrived otherwise attend chnage of status.
    :param chrdriver:
    :param users:
    :param dir_exams:
    :return:
    """
    df_exams = file_manager.get_path_files_from_folder_path(dir_exams)
    exams=sum([df_exams[col].unique().tolist() for col in df_exams.columns],[]) #get only one unique value list from df_exams

    #get oldest file last modification date
    oldest_exam_date_TS=min([os.path.getmtime(exam) for exam in exams])
    oldest_exam_date = datetime.fromtimestamp(oldest_exam_date_TS).date().strftime("%d-%m-%Y").__str__()

    chrdriver=users.login_admin(chrdriver=chrdriver)
    chrdriver.find_element(By.LINK_TEXT, "Operazioni di Amministrazione").click()
    chrdriver.find_element(By.LINK_TEXT, "Modifica Stato Esame").click()

    inser_date_start = chrdriver.find_element(By.ID, "inp_date_from")
    inser_date_start.send_keys(oldest_exam_date)
    inser_date_end = chrdriver.find_element(By.ID, "inp_date_to")
    inser_date_end.send_keys(datetime.today().date().strftime("%d-%m-%Y").__str__())
    chrdriver.find_element(By.XPATH, "//*[@id='cc_table']/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td[2]/div").click()
    chrdriver.find_element(By.LINK_TEXT, users.struttura.name).click()

    chrdriver.find_element(By.ID, "search").click()

    #Create DataFrame that is similar to platform results table
    #Get one row at time of table
    table_admin=pd.DataFrame(columns=["DO_invio", "cardio",  "nome", "DO_refertazione", "DO_registrazione", "codice_fiscale", "struttura", "stato"])
    try:
        n_exams_in_table=len(chrdriver.find_elements(By.XPATH, "/html/body/div[4]/div/div/div/form/table[2]/tbody/tr"))
        index=1
        while index < n_exams_in_table:
            print(f"While:\n \t {index}")
            chrdriver.find_element(By.ID, "search").click()
            list_exams_in_t=chrdriver.find_elements(By.XPATH, "/html/body/div[4]/div/div/div/form/table[2]/tbody/tr")
            list_from_index=list_exams_in_t[index:]
            for exam in list_from_index:  # first one is col_names
                print(index)
                tds = exam.find_elements(By.TAG_NAME, "td")
                new_row=[td.text for td in tds[1:8]]
                #get status
                opt_status_t = exam.find_elements(By.TAG_NAME, "option")
                for opt in opt_status_t:
                    if opt.get_attribute("selected"):
                        status_t = opt.text
                #control if in lavorazione
                if status_t == "InLavorazione":
                    time.sleep(5)
                    break
                index += 1
                new_row.append(status_t)
                table_admin.loc[len(table_admin)]=new_row
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        filename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        print(f"Error in {filename}, row {line_number}")
    print("")
    #table_admin.set_index('cf')
    return table_admin

def download_wait(path_to_downloads, df_esame: pd.DataFrame):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 30:
        time.sleep(1)
        for fname in os.listdir(path_to_downloads):
            if df_esame.loc["file_exam"] in ["borsam", "BORSAM"]:
                if fname.endswith("ACecg"):
                    dl_wait = False
            elif fname.endswith(df_esame.loc["file_exam"]):
                dl_wait = False
        seconds += 1
    if seconds < 30:
        print(f"\tFile downloaded correctly \n")
        return 0
    else:
        print(f"\tFile NOT downloaded after {seconds} sec \n")
        return 1

def label_encoder(encode_param: dict, to_encode: list):
    """
    Simply takes dict with labels and corresponding value, and a ist that contains values to encode. Iterate on list_toencode
    and iterate on dictionary, when elem is equal to val_dict, append to return list
    :param encode_param:
    :param to_encode:
    :return:
    """
    return [lbl for elem in to_encode for val, lbl in zip(encode_param.values(), encode_param.keys()) if elem==val]

def age(birthdate: str):
    birthdate=datetime.strptime(birthdate.replace("-","/"), '%d/%m/%Y')
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age




