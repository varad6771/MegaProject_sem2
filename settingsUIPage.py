import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
#import createSettings as cs


class settingsPage(Gtk.Window):


    def gtk_main_quit(self, widget, data=None):
        Gtk.main_quit()


    def save_func(self, widget, data=None):
        print("in save_func")

    def reset_func(self, widget, data=None):
        print("in reset_func")
        self.entry_app1.set_text("")
        self.entry_app2.set_text("")
        self.entry_app3.set_text("")
        self.entry_pwd.set_text("")

        uname = cs.get_uname()
        print("uname in settingsPage "+uname)
        fname = uname+".json"
        print(fname)
        if cs.file_reset(fname) == True:
            print("settings reseted successfully")
        else:
            print("settings reset failed")

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("SettingsForm1.glade")
        self.window = builder.get_object("window2")
        self.entry_app1 = builder.get_object("entry_app1")
        self.entry_app2 = builder.get_object("entry_app2")
        self.entry_app3 = builder.get_object("entry_app3")
        self.entry_pwd = builder.get_object("entry_pwd")
        
        self.window.connect("destroy", Gtk.main_quit)
        builder.connect_signals(self)


win = settingsPage()
win.show_all()
Gtk.main()
