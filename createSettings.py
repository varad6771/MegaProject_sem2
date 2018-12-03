import json
from pathlib import Path

'''
    This function writes the settings in settings.json
    if the file is not there it will create the file and then store function else it will read settings
    @params input_name, input_password, app1, app2, app3
 '''
 # TODO: to take the password in secure form instead of plaintext
def write_settings(input_name,input_password,app1,app2,app3):

    data = {}
    data['Settings'] = []
    data['Settings'].append({
        'name': input_name,
        'password': input_password,
        'app1': app1,
        'app2': app2,
        'app3': app3,
    })

    '''
        TODO:
        first check whether folder is there then check whether file is there
        check the path depending upon where a folder will be created
        folder will be used to store some of the important settings and other tidbits
    '''

    settingsFile = Path("settings.json")
    if settingsFile.is_file():
        print("File is present") # do some processing
    else:
        with open('settings.json', 'w') as outfile:
            json.dump(data, outfile) # settings written to file


'''
    This function reads the data from file.
    @return array of settings :- input_data[]
'''
def read_settings():

    with open('settings.json') as json_file:
        input_data = json.load(json_file)

    return input_data


# if __name__ == '__main__':
#     write_settings('varad', 'vanjape', '$HOME/Code/MegaProject_sem2/app1','$HOME/Code/MegaProject_sem2/app2','$HOME/Code/MegaProject_sem2/app3')
#     read_settings()
# example of how to access the data from file
# for settings_data_file in input_data['Settings']:
#     print('Name: ' + settings_data_file['name'])
#     print('Password: ' + settings_data_file['password'])
#     print('app1: ' + settings_data_file['app1'])
#     print('app2: ' + settings_data_file['app2'])
#     print('app3: ' + settings_data_file['app3'])
#     print('')
