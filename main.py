import github_version, microsoft, cmake, git_version, ipmiutil, lss, python, pypi
import json
import pandas as pd
from time import sleep
import os


list = json.load(open("test_list.json"))
output = []

def add_to_output(Name, current_version, latest_minor, latest_version):
    global output
    output.append([Name, current_version, latest_minor, latest_version])
    
def print_output():
    df = pd.DataFrame(output, columns=['Name', "Current Version", "Latest Minor", "Latest Version"])
    print(df)
    
def get_parser(i):
    if list["elements"][i]["parser"] == "github":
        return
        try:
            
            result = github_version.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], list["elements"][i]["by_date"])
            add_to_output(result[0], result[1])
        except KeyError:
            result = github_version.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], False)
            add_to_output(result[0], result[1])
            
            
    elif list["elements"][i]["parser"] == "microsoft":
        result = microsoft.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], list["elements"][i]["name"], by_minor=True)
        add_to_output(result[0], result[1], result[2], result[3])
        
    elif list["elements"][i]["parser"] == "cmake":
        result = cmake.main(list["elements"][i]["url"], list["elements"][i]["current_version"])
        add_to_output(result[0], result[1], result[2], result[3])
        
    # elif list["elements"][i]["parser"] == "git":
    #     result = git_version.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"])
    #     add_to_output(result[0], result[1], result[2])
        
    elif list["elements"][i]["parser"] == "ipmiutil":
        result = ipmiutil.main(list["elements"][i]["url"], list["elements"][i]["current_version"], by_major=list["elements"][i]["by_major"], by_minor=list["elements"][i]["by_minor"])  
        add_to_output(result[0], result[1], result[2], result[3])
          
    elif list["elements"][i]["parser"] == "lss":
        result = lss.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"])
        add_to_output(result[0], result[1], result[2], result[3])
                
    elif list["elements"][i]["parser"] == "python":
        result = python.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], by_major=list["elements"][i]["by_major"], by_minor=list["elements"][i]["by_minor"])
        add_to_output(result[0], result[1], result[2], result[3])
         
    elif list["elements"][i]["parser"] == "pypi":
        try:
            result = pypi.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], beta=list["elements"][i]["beta"], by_major=list["elements"][i]["by_major"], by_minor=list["elements"][i]["by_minor"])
            if len(result) == 3:
                add_to_output(result[0], result[1], result[2], result[3])
            else:
                add_to_output(result[0], result[1], result[2], result[3])
        except:
            result = pypi.check_version(list["elements"][i]["url"], list["elements"][i]["current_version"], False, by_major=True, by_minor=False)
            if len(result) == 3:
                add_to_output(result[0], result[1], result[2], result[3])
            else:
                add_to_output(result[0], result[1], result[2], result[3])
            
        

while True:            
    for i in range(len(list["elements"])):
        get_parser(i)
    os.system('cls' if os.name == 'nt' else 'clear')
    print_output()
    output = []
    sleep(10)

