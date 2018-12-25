import json
import os
from pathlib import Path


'''
    TODO: to take the password in secure form instead of plaintext
    TODO: also we will need to change this and other functions to create files in specific folder 
    currently we are considering the folder is same for every body and hence checking settings file in current
    folder
'''

#settings_file = Path("settings.json")
input_name = ""
input_password = ""

'''
    This function writes the settings in settings.json
    if the file is not there it will create the file and then store function else it will read settings
    @params input_name, input_password, app1, app2, app3
 '''
def write_settings(input_name, input_password, app1, app2, app3):
    #print("in write_settings func vals of param comin up")
    #print(input_name)
    #print(input_password)
    #print(app1)
    #print(app2)
    #print(app3)

    data = {}
    data['Settings'] = []
    data['Settings'].append({
        'name': input_name,
        'password': input_password,
        'app1': app1,
        'app2': app2,
        'app3': app3,
    })

    out_fname = input_name+".json" 
    # print(out_fname)
    with open(out_fname, 'w') as outfile:
        json.dump(data, outfile) 

    return out_fname


'''
    This function reads the data from file.
    @return array of settings :- input_data[]
'''
def read_settings(in_fname):
    #print("in createSettings and in read_settings")
    
    with open(in_fname, 'r') as json_file:
        input_data = json.load(json_file)
    
    return input_data

def file_existence(in_fname):
    #print(in_file)
    settings_file = Path(in_fname)
    if settings_file.exists():
        return True
    
    return False

def file_reset(in_fname):
    #print("in file reset func in createSettings")
    #print("name received is  "+in_fname)
    os.remove(in_fname)
    if file_existence(in_fname):
       # print("file deleted")
        return False
    
    #print("file exist")
    return True


