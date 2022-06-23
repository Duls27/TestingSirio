import pandas as pd
import os
"""
file_manager contain function to work with external file and external folders
"""

def get_path_files_from_folder_path (folder_path: str):
    """
    Thi function return a DataFrame with examns contained in folder_path. If single exam, single value, if folder, all exams in folder
    :param folder_path: string with path
    :return: DataFrame
    """
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
