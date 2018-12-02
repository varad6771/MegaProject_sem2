import json
from pathlib import Path


def write_settings():
    # TODO :- take input as args from other function. Args would be name, paswd, and 3 subproc args

    input_name = input("Enter the name")
    input_password = input("Enter the password")

    print(input_name)
    print(input_password)

    data = {}
    data['Settings'] = []
    data['Settings'].append({
        'name': input_name,
        'password': input_password,
    })

    ''' 
        first check whether folder is there then check whether file is there
        check the path depending upon where a folder will be created
        folder will be used to store some of the important settings and other tidbits
    '''

    settingsFile = Path("settings.json")
    if settingsFile.is_file():
        print("File is present")
        read_settings()
    else:
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile)


def read_settings():
    print("in read settings")
    with open('settings.json') as json_file:
        input_data = json.load(json_file)
    for p in input_data['Settings']:
        print('Name: ' + p['name'])
        print('Password: ' + p['password'])
        print('')
    # TODO :- pass read subprocess args to another function


if __name__ == '__main__':
    write_settings()
    read_settings()
