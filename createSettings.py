from passlib.context import CryptContext

import json
import os
import os.path

uname = ""
pwd = ""


def write_settings(input_name, input_password, app1, app2, app3, app4, app5):
    """
    writes settings to file in json format
        :param input_name: 
        :param input_password: 
        :param app1: 
        :param app2: 
        :param app3:
        :param app4:
        :param app5: 
        @return string:
    """
    data = {}
    data['Settings'] = []
    data['Settings'].append({
        'name': input_name,
        'password': input_password,
        'app1': app1,
        'app2': app2,
        'app3': app3,
        'app4': app4,
        'app5': app5,
    })

    out_fname = input_name+".json" 

    with open(out_fname, 'w') as outfile:
        json.dump(data, outfile) 

    return out_fname


def read_settings(in_fname):
    """
    writes settings to file in json format
        :param in_fname: 
        @return array:
    """
    with open(in_fname, 'r') as json_file:
        input_data = json.load(json_file)
    return input_data


def file_existence(in_fname):
    """
    check the existence of file
        :param in_fname: 
        @return boolean:
    """
    if os.path.isfile(in_fname):
        return True
    
    return False



def file_reset(in_fname):
    """
    remove (reset) the file from path
        :param in_fname:
        @return boolean: 
    """
    os.remove(in_fname)
    if file_existence(in_fname):
        return False
    
    return True


def encrypt(raw):
    """
    encrypt the password
        :param raw:
        @return hash: 
    """
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
    )
    return pwd_context.encrypt(raw)


def checkPwd(red_pwd, inp_pwd):
    """
    check passwords
        :param red_pwd: 
        :param inp_pwd: 
        @return boolean:
    """
    pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=3000
    )
    return pwd_context.verify(inp_pwd, red_pwd)


def checkUnm(red_unm, inp_unm):
    """
    check uname
        :param red_unm: 
        :param inp_unm:
        @return boolean:
    """
    if red_unm == inp_unm:
        return True

    return False


def checkEmpty(field_val):
    """
    check empty fields
        :param field_val:
        @return boolean:
    """
    if field_val == "":
        return True

    return False


def set_uname(input_uname):
    global uname
    uname = input_uname


def set_pwd(input_pwd):
    global pwd
    pwd = input_pwd


def get_pwd():
    print(pwd)
    return pwd


def get_uname():
    print(uname)
    return uname