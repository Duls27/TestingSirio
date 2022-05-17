import pandas as pd
import os

#This function use Panda library for extract info from excel file
#INPUT: path to excel file, and aheet name
#OUTPUT: data frames with data for each excell sheet
def get_info_from_excel (path_bootstrap, sheet_name):
    df = pd.read_excel(path_bootstrap,sheet_name=sheet_name)
    return df

def get_path_files_exams_from_folder_path (exam_folder_path):
    exams_dict = {}
    exam_list=os.listdir(path=exam_folder_path)
    for is_it_exam in exam_list:
        if is_it_exam.__contains__("."):
            extension=is_it_exam.split(sep=".")[1]
            exams_dict[extension]=exam_folder_path + '/' + is_it_exam

        else:
            exams_dict[is_it_exam]= [(exam_folder_path + '/' + is_it_exam + '/') + s for s in os.listdir(path=exam_folder_path + '/' + is_it_exam)] #appending exam_folder path to every element in list of element in folder

    df=pd.DataFrame(data=exams_dict)
    return df

