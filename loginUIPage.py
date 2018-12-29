import gi
import createSettings as cs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# TODO: hide previous window after opening of next one and code cleanup
# TODO: set_text() to app prefs in settings page
# TODO: add dialogues in place of print() at 
'''
    1) login_func() pass/fail login
    2) register_func() to set app prefs and pass/fail reg
    3) save_func() settings save/fail
    4) reset_func() reset fail/fail and please set new settings
'''


class loginPage(Gtk.Window):

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def login_func(self, widget, data=None):
        global input_uname
        
        input_uname = self.entry_uname.get_text()
        input_pwd  = self.entry_pwd.get_text()
        print(input_uname)
        print(input_pwd)

        in_file = input_uname+".json"   

        if cs.file_existence(in_file) == False:
            print("file does not exist so login fail")
        else:
            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:
                if data_file['name'] == input_uname and data_file['password'] == input_pwd :
                    print("login success")
            
                    builder = Gtk.Builder()
                    builder.add_from_file("DashboardForm1.glade")
                    self.window = builder.get_object("window2")
                    builder.connect_signals(self)
                    self.window.show_all()
                    print("on DashboardForm1")
                else:
                    print("login failed")

    def clear_func(self, widget, data=None):
        print("in clear_func")
        input_uname = self.entry_uname.set_text("")
        input_pwd  = self.entry_pwd.set_text("")

    def register_func(self, widget, data=None):
        print("in register_func")
        uname_val = self.entry_uname.get_text()
        pwd_val  = self.entry_pwd.get_text() 
        print(uname_val)
        print(pwd_val)

        in_file = uname_val+".json"
        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            created_settings_file = cs.write_settings(uname_val, pwd_val, "abc", "abc", "abc")    
            print("register successful file created  "+created_settings_file)
            print(" please add the app prefs in settings")
            uname_val = self.entry_uname.set_text("")
            pwd_val  = self.entry_pwd.set_text("")
        else:
            input_data = cs.read_settings(in_file)
            for settings_data_file in input_data['Settings']:  
                if settings_data_file['name'] == uname_val:
                    print("data exist! you cannot re-register")
                    break

    def save_func(self, widget, data=None):
        print("in save_func")
        print("input uname after login "+input_uname)
        val1 = self.entry_app1.get_text()
        val2 = self.entry_app2.get_text()
        val3 = self.entry_app3.get_text()
        val4 = self.entry_pwd_s.get_text()
        created_settings_file = cs.write_settings(input_uname, val4, val1, val2, val3)
        if cs.file_existence(created_settings_file) == True:
            print("settings saved file name   "+created_settings_file)
        else:
            print("settings save failed and file doesn't exist")

    def reset_func(self, widget, data=None):
        print("in reset_func")
        print("input uname after login "+input_uname)
        val1 = self.entry_app1.set_text("")
        val2 = self.entry_app2.set_text("")
        val3 = self.entry_app3.set_text("")
        val4 = self.entry_pwd_s.set_text("")
        reset_file_name = input_uname+".json"
        print("reset file name "+reset_file_name)
        if  cs.file_reset(reset_file_name) == True:
            print("settings reseted successfully")
        else:
            print("settings reset failed")

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




