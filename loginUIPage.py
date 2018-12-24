import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import createSettings as cs
from settingsUIPage import settingsPage


class loginPage(Gtk.Window):
    input_uname = ""
    input_pwd = ""
    created_settings_file = ""

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()


    #           TODO: now instead of print replace to dialogue and make login attempts check 3 then show error message
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
                    cs.set_uname(input_uname)
                    sp_object = settingsUIPage.settingsPage()
                    
                else:
                    print("login failed")

    def clear_func(self, widget, data=None):
        self.entry_uname.set_text("")
        self.entry_pwd.set_text("")
        input_uname = ""
        input_pwd = ""
        # print(input_uname)
        # print(input_pwd)

    #            TODO: present dialogue that data exist and cannot register and break it
    def register_func(self, widget, data=None): 
        # print("in register_func")
        uname = self.entry_uname.get_text()
        pwd  = self.entry_pwd.get_text()

        # print(uname)
        # print(pwd)

        in_file = uname+".json"
        # print("in_file for existence check  "+in_file)
        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            created_settings_file = cs.write_settings(uname, pwd, "abc", "def", "ghi")    
        else:
            input_data = cs.read_settings(in_file)
            for settings_data_file in input_data['Settings']:  
                if settings_data_file['name'] == uname:
                    print("data exist! you cannot re-register")
                    break

 



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
