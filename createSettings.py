from pathlib import Path
from passlib.context import CryptContext

import json
import os
import base64
import hashlib



'''
    TODO: also we will need to change this and other functions to create files in specific folder 
    currently we are considering the folder is same for every body and hence checking settings file in current
    folder
'''

def write_settings(input_name, input_password, app1, app2, app3):

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

    with open(out_fname, 'w') as outfile:
        json.dump(data, outfile) 

    return out_fname

def read_settings(in_fname):
    
    with open(in_fname, 'r') as json_file:
        input_data = json.load(json_file)
    
    return input_data

def file_existence(in_fname):

    settings_file = Path(in_fname)
    if settings_file.exists():
        return True
    
    return False

def file_reset(in_fname):

    os.remove(in_fname)
    if file_existence(in_fname):
        return False
    
    return True

def encrypt(raw):

    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
    )
    return pwd_context.encrypt(raw)

def checkPwd(red_pwd, inp_pwd):
 
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
    )
    return pwd_context.verify(inp_pwd, red_pwd)

def checkUnm(red_unm, inp_unm):
    
    if red_unm == inp_unm:
        return True
    
    return False
  
def checkEmpty(field_val):

    if field_val == "":
        return True
    
    return False