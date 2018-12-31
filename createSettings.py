from Crypto import Random
from Crypto.Cipher import AES
from pathlib import Path

import json
import os
import base64
import hashlib



'''
    TODO: also we will need to change this and other functions to create files in specific folder 
    currently we are considering the folder is same for every body and hence checking settings file in current
    folder
'''

input_name = ""
input_password = ""

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

def encrypt(raw,key):
    
    raw = _pad(raw)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))

def decrypt(enc,key):
    
    enc = base64.b64decode(enc)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return _unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

def _pad(s):
    bs = 32
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)

def _unpad(s):
    return s[:-ord(s[len(s)-1:])]

def checkPwd(red_pwd, inp_pwd):
    
    if red_pwd == inp_pwd:
        return True
    
    return False

def checkUnm(red_unm, inp_unm):
    
    if red_unm == inp_unm:
        return True
    
    return False
  