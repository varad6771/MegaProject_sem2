import gi
import createSettings as cs
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


# TODO: code cleanup (remaining) and code comments


class loginPage(Gtk.Window):

    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()

    def login_func(self, widget, data=None):
        global input_uname
        global input_pwd
        global in_file
        
        input_uname = self.entry_uname.get_text()
        input_pwd  = self.entry_pwd.get_text()

        in_file = input_uname+".json"   

        if cs.file_existence(in_file) == False:
            print("file does not exist so login fail")
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Login failed!! Please try again") 
            self.dialog.run()
            self.dialog.destroy()
            input_uname = self.entry_uname.set_text("")
            input_pwd  = self.entry_pwd.set_text("")
        else:
            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:

                red_pwd = data_file['password']
                red_unm = data_file['name'] 
                if cs.checkUnm(red_unm, input_uname) == True and cs.checkPwd(red_pwd, input_pwd) == True:
                    print("login success")
                    self.window2.show_all()
                    self.title_label.set_text("Welcome  "+input_uname)
                    self.window1.hide()
                    print("on DashboardForm1")
                else:
                    self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   "Wrong Credentials !! Please try again") 
                    self.dialog.run()
                    self.dialog.destroy()
                    input_uname = self.entry_uname.set_text("")
                    input_pwd  = self.entry_pwd.set_text("")

    def clear_func(self, widget, data=None):
        print("in clear_func")
        input_uname = self.entry_uname.set_text("")
        input_pwd  = self.entry_pwd.set_text("")

    def register_func(self, widget, data=None):
        print("in register_func")
        uname_val = self.entry_uname.get_text()
        pwd_val  = self.entry_pwd.get_text() 
        in_file = uname_val+".json"

        ciphertext_input = cs.encrypt(pwd_val)
        
        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            if cs.checkEmpty(uname_val) == False and cs.checkEmpty(pwd_val) == False:
                created_settings_file = cs.write_settings(uname_val, ciphertext_input, "abc", "abc", "abc")    
                print("register successful file created  "+created_settings_file)
                self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                       Gtk.DialogFlags.MODAL,
                                       Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK,
                                       "New User is Registered!! Please set app preferences in settings")
                self.dialog.run()
                self.dialog.destroy()
                uname_val = self.entry_uname.set_text("")
                pwd_val  = self.entry_pwd.set_text("")
            else:
                self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                       Gtk.DialogFlags.MODAL,
                                       Gtk.MessageType.INFO,
                                       Gtk.ButtonsType.OK,
                                       "Credential cannot be empty!! Please fill all the fields")
                self.dialog.run()
                self.dialog.destroy()
        else:
            input_data = cs.read_settings(in_file)
            for settings_data_file in input_data['Settings']:  
                if settings_data_file['name'] == uname_val:
                    print("data exist! you cannot re-register")
                    self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   "User Already Exists!! You cannot Re-Register")
                    self.dialog.run()
                    self.dialog.destroy()
                    break

    def save_func(self, widget, data=None):
        print("in save_func")
        val1 = self.entry_app1.get_text()
        val2 = self.entry_app2.get_text()
        val3 = self.entry_app3.get_text()
        val4 = self.entry_pwd_s.get_text()

        if cs.checkEmpty(val4) == True:
            val4 = input_pwd
        else:
            val4 = self.entry_pwd_s.get_text()

        if cs.checkEmpty(val1) == False and cs.checkEmpty(val2) == False and cs.checkEmpty(val3) == False:
            ciphertext_input = cs.encrypt(val4)
            created_settings_file = cs.write_settings(input_uname, ciphertext_input, val1, val2, val3)
        else:
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Fields cannot be empty!! Please fill all the fields")
            self.dialog.run()
            self.dialog.destroy()
            


        if cs.file_existence(created_settings_file) == True:
            print("settings saved file name   "+created_settings_file)
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "New Settings are Updated Successfully ")
            self.dialog.run()
            self.dialog.destroy()
        else:
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   "New Settings are not Updated!! Please try again later")
            self.dialog.run()
            self.dialog.destroy()

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
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK,
                                   "Settings Reset Success!! Please enter new settings")
            self.dialog.run()
            self.dialog.destroy()
        else:
            self.dialog = Gtk.MessageDialog(Gtk.Window(), 
                                   Gtk.DialogFlags.MODAL,
                                   Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.OK,
                                   "Settings Reset Failed")
            self.dialog.run()
            self.dialog.destroy()

    def run_app_func(self, widget, data=None):
        print("in run_app_func")
        self.window2.hide()

    def goto_settings_func(self, widget, data=None):
        print("in goto_settings_func")
      
        input_data = cs.read_settings(in_file)
        for data_file in input_data['Settings']:
            var1 = data_file['app1']
            var2 = data_file['app2']
            var3 = data_file['app3']

        self.entry_app1.set_text(var1)
        self.entry_app2.set_text(var2)
        self.entry_app3.set_text(var3)
        self.uname_label.set_text(input_uname)
        self.window3.show_all()
        self.window2.hide()

    def back_func(self, widget, data=None):
        print("in back_func")
        self.window2.show_all()
        self.window3.hide()

    def __init__(self):
        
        # Login Page
        builder = Gtk.Builder()
        builder.add_from_file("LoginForm1.glade")
        self.window1 = builder.get_object("window1")
        self.window1.show_all()
        self.window1.connect("destroy", Gtk.main_quit)
        builder.connect_signals(self)

        # Settings Page
        builder1 = Gtk.Builder()
        builder1.add_from_file("SettingsForm1.glade")
        self.window3 = builder1.get_object("window3")
        self.window3.connect("destroy", Gtk.main_quit)
        builder1.connect_signals(self)

        # Dashboard Page
        builder2 = Gtk.Builder()
        builder2.add_from_file("DashboardForm1.glade")
        self.window2 = builder2.get_object("window2")
        self.window2.connect("destroy", Gtk.main_quit)
        builder2.connect_signals(self)



        # Dashboard Page imports
        self.title_label = builder2.get_object("label_title")
        # Settings Page imports
        self.entry_app1 = builder1.get_object("entry_app1")
        self.entry_app2 = builder1.get_object("entry_app2")
        self.entry_app3 = builder1.get_object("entry_app3")
        self.entry_pwd_s = builder1.get_object("entry_pwd_s")
        self.uname_label = builder1.get_object("label_uname")
        # Login Page imports
        self.entry_uname = builder.get_object("entry_uname")
        self.entry_pwd = builder.get_object("entry_pwd")
        


lp_win = loginPage()
Gtk.main()




