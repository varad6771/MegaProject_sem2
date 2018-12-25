import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import createSettings as cs


class loginPage(Gtk.Window):
    input_uname = ""
    input_pwd = ""
    created_settings_file = ""

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()
    
    '''
        TODO: now instead of print replace to dialogue and make login attempts check 3 then show error message
        TODO: after login success pls move to settingsPage for now and later add a landing page
        TODO: display error msg for failed login
    '''
    def login_func(self, widget, data=None):
        input_uname = self.entry_uname.get_text()
        input_pwd  = self.entry_pwd.get_text()
        # print(input_uname)
        # print(input_pwd)

        in_file = input_uname+".json"
        
        if cs.file_existence(in_file) == False:
            print("file does not exist so login might fail")
        else:
            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:
                if data_file['name'] == input_uname and data_file['password'] == input_pwd :
                    print("login success")
                    global reset_file_name
                    global final_uname
                    reset_file_name = input_uname+".json"
                    uname = input_uname
                    
                    builder = Gtk.Builder()
                    builder.add_from_file("SettingsForm1.glade")
                    self.window = builder.get_object("window3")
                    self.entry_app1 = builder.get_object("entry_app1")
                    self.entry_app2 = builder.get_object("entry_app2")
                    self.entry_app3 = builder.get_object("entry_app3")
                    self.entry_pwd_s = builder.get_object("entry_pwd_s")
                    builder.connect_signals(self)
                    self.window.show_all()
                    
                    
                    # builder2 = Gtk.Builder()
                    # builder2.add_from_file("DashboardForm1.glade")
                    # self.window = builder2.get_object("window2")
                    # self.window.show_all()
                     
                else:
                    print("login failed")

    def clear_func(self, widget, data=None):
        self.entry_uname.set_text("")
        self.entry_pwd.set_text("")
        input_uname = ""
        input_pwd = ""

    '''
        TODO: present dialogue that data exist and cannot register and break it
        TODO: also take the app1, app2, app3 preferences or rather ask user to 
        set it in settings after first login
    '''
    def register_func(self, widget, data=None): 
        uname = self.entry_uname.get_text()
        pwd  = self.entry_pwd.get_text()
        self.entry_uname.set_text("")
        self.entry_pwd.set_text("")
        in_file = uname+".json"
        
        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            created_settings_file = cs.write_settings(uname, pwd, "abc", "def", "ghi")    
        else:
            input_data = cs.read_settings(in_file)
            for settings_data_file in input_data['Settings']:  
                if settings_data_file['name'] == uname:
                    print("data exist! you cannot re-register")
                    break

    def save_func(self, widget, data=None):
        print("in save_func")
        entry_app1_val = self.entry_app1.get_text()
        entry_app2_val = self.entry_app2.get_text()
        entry_app3_val = self.entry_app3.get_text()
        entry_pwd_s_val = self.entry_pwd_s.get_text()

        print("values of app1  "+entry_app1_val)
        print("values of app2  "+entry_app2_val)
        print("values of app3  "+entry_app3_val)
        print("values of password  "+entry_pwd_s_val)
        print("val of final_uname in save func  "+final_uname)


        created_settings_file = cs.write_settings(final_uname, entry_pwd_s_val, entry_app1_val, entry_app2_val, entry_app3_val)
        if cs.file_existence(created_settings_file) == True:
            print("settings saved")
        else:
            print("settings save failed and file doesn't exist")

    #           TODO: present dialogue that reset success and break it
    def reset_func(self, widget, data=None):
        print("in reset_func")
        self.entry_app1.set_text("")
        self.entry_app2.set_text("")
        self.entry_app3.set_text("")
        self.entry_pwd_s.set_text("")
        print("value of reset_file_name in reset func in loginPage   "+reset_file_name)

        if  cs.file_reset(reset_file_name):
            print("settings reseted successfully")
        else:
            print("settings reset failed")

    #           TODO: write a call to execute the rest of application
    def run_app_func(self, widget, data=None):
        print("in run_app_func")
    
    def goto_settings_func(self, widget, data=None):
        print("in goto_settings_func")
        
        builder = Gtk.Builder()
        builder.add_from_file("SettingsForm1.glade")
        self.window = builder.get_object("window3")
        self.entry_app1 = builder.get_object("entry_app1")
        self.entry_app2 = builder.get_object("entry_app2")
        self.entry_app3 = builder.get_object("entry_app3")
        self.entry_pwd_s = builder.get_object("entry_pwd_s")
        builder.connect_signals(self)
        self.window.show_all()


    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("LoginForm1.glade")
        self.window = builder.get_object("window1")
        self.window.show_all()
        self.window.connect("destroy", Gtk.main_quit)
        self.entry_uname = builder.get_object("entry_uname")
        self.entry_pwd = builder.get_object("entry_pwd")
        builder.connect_signals(self)



lp_win = loginPage()
Gtk.main()




