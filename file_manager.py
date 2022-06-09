import pandas as pd
import os

#This function use Panda library for extract info from excel file
#INPUT: path to excel file, and aheet name
#OUTPUT: data frames with data for each excell sheet
def get_info_from_excel (path_bootstrap, sheet_name):
    df = pd.read_excel(path_bootstrap,sheet_name=sheet_name)
    return df

def get_path_files_from_folder_path (folder_path):
    folder_dict = {}
    file_list=os.listdir(path=folder_path)
    flag_folder=0
    for is_it_file in file_list:
        if is_it_file.__contains__("."):
            extension=is_it_file.split(sep=".")[1]
            folder_dict[extension]=folder_path + '/' + is_it_file

        else:
            flag_folder=1
            folder_dict[is_it_file]= [(folder_path + '/' + is_it_file + '/') + s for s in os.listdir(path=folder_path + '/' + is_it_file)] #appending exam_folder path to every element in list of element in folder

    if flag_folder==1:
        df = pd.DataFrame(data=folder_dict)
    else:
        df = pd.DataFrame(data=folder_dict, index=[0])

    return df
