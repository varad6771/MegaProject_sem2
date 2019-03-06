import tkinter as tk
import createSettings as cs
import detection as det

from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkfont


class LoginForm(tk.Frame):

    def login_func(self):
        input_uname = self.entry_username.get()
        input_pwd = self.entry_password.get()

        in_file = input_uname + ".json"

        if cs.file_existence(in_file) is False:
            print("file does not exist so login fail")
            messagebox.showerror("Login Fail", "User does not Exist")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            self.controller.app_data["Username"].set(input_uname)
            self.controller.app_data["in_file"].set(in_file) 
            self.controller.app_data["password"].set(input_pwd)

            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:
                
                red_pwd = data_file['password']
                red_unm = data_file['name']
                if cs.check_unm(red_unm, input_uname) is True and cs.check_pswd(red_pwd, input_pwd) is True:
                    print("login success")
                    self.controller.app_data["app_1"].set(data_file['app1']) 
                    self.controller.app_data["app_2"].set(data_file['app2'])
                    self.controller.app_data["app_3"].set(data_file['app3'])
                    self.controller.app_data["app_4"].set(data_file['app4'])
                    self.controller.app_data["app_5"].set(data_file['app5'])
                    self.controller.show_frame("DashboardForm")
                    print("on DashboardForm1")
                else:
                    messagebox.showerror("Login error", "Incorrect Credentials")
                    input_uname = self.entry_username.delete(0, tk.END)
                    input_pwd = self.entry_password.delete(0, tk.END)

    def clear_func(self):
        print("in clear func")
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.grid(row=0)
        self.label_password.grid(row=1)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        loginbtn = tk.Button(self, text="Login", command=self.login_func)
        loginbtn.grid(row=2, column=0)

        registerbtn = tk.Button(self, text="Registration", command=lambda: controller.show_frame("RegisterForm"))
        registerbtn.grid(row=2, column=1)

        clearbtn = tk.Button(self, text="Clear", command=self.clear_func)
        clearbtn.grid(row=2, column=2)

        self.pack()


class RegisterForm(tk.Frame):
    
    def register_func(self):
        print("in register_func")
        uname_val = self.entry_username.get()
        pwd_val = self.entry_password.get()
        pwd_re_val = self.entry_password_reenter.get()

        if cs.check_empty(pwd_re_val) is True:
            messagebox.showerror("Empty Credentials", "Please fill all the fields")
        elif pwd_re_val != pwd_val:
            messagebox.showerror("Password do not match", "Please enter same password")
        else:
            in_file = uname_val + ".json"
            ciphertext_input = cs.encrypt(pwd_val)
            if cs.file_existence(in_file) is False:
                print("file does not exist so write settings")
                if cs.check_empty(uname_val) is False and cs.check_empty(pwd_val) is False:
                    created_settings_file = cs.write_settings(uname_val, ciphertext_input, "abc", "abc", "abc", "abc",
                                                              "abc")
                    print("register successful file created  " + created_settings_file)
                    messagebox.showinfo("Register Succesful", "Please set app preferences in settings")
                    self.entry_username.delete(0, tk.END)
                    self.entry_password.delete(0, tk.END)
                    self.entry_password_reenter.delete(0, tk.END)
                else:
                    messagebox.showerror("Empty Credentials", "Please fill all the fields")
            else:
                input_data = cs.read_settings(in_file)
                for settings_data_file in input_data['Settings']:
                    if settings_data_file['name'] == uname_val:
                        print("data exist! you cannot re-register")
                        messagebox.showerror("Error", "User Already Exists!! You cannot Re-Register")
                        break

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")
        self.label_password_reenter = tk.Label(self, text="Re enter Password")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password_reenter = tk.Entry(self, show="*")

        self.label_username.grid(row=0)
        self.label_password.grid(row=1)
        self.label_password_reenter.grid(row=2)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        self.entry_password_reenter.grid(row=2, column=1)

        registerbtn = tk.Button(self, text="Register", command=self.register_func)
        registerbtn.grid(row=3, column=1)

        loginbtn = tk.Button(self, text="Login", command=lambda: controller.show_frame("LoginForm"))
        loginbtn.grid(row=3)


class DashboardForm(tk.Frame):

    def runapp_func(self):
        print("In the run app func")
        app1_dbf = self.controller.app_data["app_1"].get()
        app2_dbf = self.controller.app_data["app_2"].get()
        app3_dbf = self.controller.app_data["app_3"].get()
        app4_dbf = self.controller.app_data["app_4"].get()
        app5_dbf = self.controller.app_data["app_5"].get()
        det.get_user_prefs(app1_dbf, app2_dbf, app3_dbf, app4_dbf, app5_dbf)
        det.detect()
        det.predict()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        runappbtn = tk.Button(self, text="Run app", command=self.runapp_func)
        runappbtn.grid(row=1, column=0)

        settingsbtn = tk.Button(self, text="Settings Page", command=lambda: controller.show_frame("SettingsForm"))
        settingsbtn.grid(row=1, column=1)

        helpbtn = tk.Button(self, text="Help Page", command=lambda: controller.show_frame("HelpForm"))
        helpbtn.grid(row=1, column=2)


class SettingsForm(tk.Frame):

    def sel_app1_func(self):
        global entry_app_var1
        self.entry_app1.delete(0, tk.END)
        entry_app_var1 = filedialog.askopenfilename(filetypes=[("exe file", "*.exe")])
        self.entry_app1.insert(0, entry_app_var1)

    def sel_app2_func(self):
        global entry_app_var2
        self.entry_app2.delete(0, tk.END)
        entry_app_var2 = filedialog.askopenfilename(filetypes=[("exe file", "*.exe")])
        self.entry_app2.insert(0, entry_app_var2)

    def sel_app3_func(self):
        global entry_app_var3
        self.entry_app3.delete(0, tk.END)
        entry_app_var3 = filedialog.askopenfilename(filetypes=[("exe file", "*.exe")])
        self.entry_app3.insert(0, entry_app_var3)

    def sel_app4_func(self):
        global entry_app_var4
        self.entry_app4.delete(0, tk.END)
        entry_app_var4 = filedialog.askopenfilename(filetypes=[("exe file", "*.exe")])
        self.entry_app4.insert(0, entry_app_var4)

    def sel_app5_func(self):
        global entry_app_var5
        self.entry_app5.delete(0, tk.END)
        entry_app_var5 = filedialog.askopenfilename(filetypes=[("exe file", "*.exe")])
        self.entry_app5.insert(0, entry_app_var5)

    def save_func(self):
        print("in save_func")
        valp = self.entry_app1.get()
        print(valp)
        print(cs.check_empty(self.entry_app1.get()))
        if cs.check_empty(self.entry_app1.get()) is True:
            print("fields are empty")
            messagebox.showerror("Empty Fields", "Please fill all the fields")
        else:
            # entry_app_var1 = self.entry_app1.get()
            # entry_app_var2 = self.entry_app2.get()
            # entry_app_var3 = self.entry_app3.get()
            # entry_app_var4 = self.entry_app4.get()
            # entry_app_var5 = self.entry_app5.get()
            global entry_passwd_var6
            entry_passwd_var6 = self.entry_password_settingsui.get()

            input_uname = self.controller.app_data["Username"].get()
            input_pwd = self.controller.app_data["password"].get()
            # print(input_pwd)

            if cs.check_empty(entry_passwd_var6) is True:
                entry_passwd_var6 = input_pwd
                # print("in check_empty")
                # print(entry_passwd_var6)
            else:
                entry_passwd_var6 = self.entry_password_settingsui.get()

            if cs.check_empty(entry_app_var1) is False and cs.check_empty(entry_app_var2) is False and cs.check_empty(
                    entry_app_var3) is False and cs.check_empty(entry_app_var4) is False and cs.check_empty(
                    entry_app_var5) is False:
                ciphertext_input = cs.encrypt(entry_passwd_var6)
                created_settings_file = cs.write_settings(input_uname, ciphertext_input, entry_app_var1, entry_app_var2,
                                                          entry_app_var3, entry_app_var4, entry_app_var5)
            else:
                messagebox.showerror("Empty Fields", "Please fill all the fields")

            if cs.file_existence(created_settings_file) is True:
                self.controller.app_data["app_1"].set(entry_app_var1) 
                self.controller.app_data["app_2"].set(entry_app_var2)
                self.controller.app_data["app_3"].set(entry_app_var3)
                self.controller.app_data["app_4"].set(entry_app_var4)
                self.controller.app_data["app_5"].set(entry_app_var5)
                self.controller.app_data["password"].set(entry_passwd_var6)
                print("settings saved file name   " + created_settings_file)
                messagebox.showinfo("Save Succesful", "New Settings are Updated Successfully ")
            else:
                messagebox.showerror("Update Failed", "New Settings are not Updated!! Please try again later")

    def reset_func(self):
        print("in reset_func")
        self.entry_app1.delete(0, tk.END)
        self.entry_app2.delete(0, tk.END)
        self.entry_app3.delete(0, tk.END)
        self.entry_app4.delete(0, tk.END)
        self.entry_app5.delete(0, tk.END)
        self.entry_password_settingsui.delete(0, tk.END)
        
        self.controller.app_data["app_1"].set("abc")
        self.controller.app_data["app_2"].set("abc")
        self.controller.app_data["app_3"].set("abc")
        self.controller.app_data["app_4"].set("abc")
        self.controller.app_data["app_5"].set("abc")

        in_file = self.controller.app_data["in_file"].get()
        print("reset file name " + in_file)

        if cs.file_reset(in_file) is True:
            messagebox.showinfo("Succesful Reset", "Settings Reseted!! Please enter new settings before logging out ")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed. Please try again")

    def reload_app_func(self):
        varchck = self.entry_app1.get()
        self.label_uname_display.config(text=self.controller.app_data["Username"].get())
        
        if cs.check_empty(varchck) is True:
            self.entry_app1.insert(0, self.controller.app_data["app_1"].get())
            self.entry_app2.insert(0, self.controller.app_data["app_2"].get())
            self.entry_app3.insert(0, self.controller.app_data["app_3"].get())
            self.entry_app4.insert(0, self.controller.app_data["app_4"].get())
            self.entry_app5.insert(0, self.controller.app_data["app_5"].get())
        
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_app1 = tk.Label(self, text="Application 1")
        self.label_app2 = tk.Label(self, text="Application 2")
        self.label_app3 = tk.Label(self, text="Application 3")
        self.label_app4 = tk.Label(self, text="Application 4")
        self.label_app5 = tk.Label(self, text="Application 5")
        self.label_uname = tk.Label(self, text="Username")
        self.label_uname_display = tk.Label(self, text="val_uname")
        self.label_password_settingsui = tk.Label(self, text="Password")

        self.entry_app1 = tk.Entry(self)
        self.entry_app2 = tk.Entry(self)
        self.entry_app3 = tk.Entry(self)
        self.entry_app4 = tk.Entry(self)
        self.entry_app5 = tk.Entry(self)
        self.entry_password_settingsui = tk.Entry(self, show="*")

        self.label_app1.grid(row=0)
        self.label_app2.grid(row=1)
        self.label_app3.grid(row=2)
        self.label_app4.grid(row=3)
        self.label_app5.grid(row=4)
        self.label_uname.grid(row=5)
        self.label_uname_display.grid(row=5, column=1)
        self.label_password_settingsui.grid(row=6)

        self.entry_app1.grid(row=0, column=1)
        self.entry_app2.grid(row=1, column=1)
        self.entry_app3.grid(row=2, column=1)
        self.entry_app4.grid(row=3, column=1)
        self.entry_app5.grid(row=4, column=1)
        self.entry_password_settingsui.grid(row=6, column=1)

        resetbtn = tk.Button(self, text="Reset", command=self.reset_func)
        resetbtn.grid(row=7, column=0)

        savebtn = tk.Button(self, text="Save", command=self.save_func)
        savebtn.grid(row=7, column=1)

        backbtn = tk.Button(self, text="Back", command=lambda: controller.show_frame("DashboardForm"))
        backbtn.grid(row=7, column=2)

        sel_app1btn = tk.Button(self, text="Select", command=self.sel_app1_func)
        sel_app1btn.grid(row=0, column=2)
        sel_app2btn = tk.Button(self, text="Select", command=self.sel_app2_func)
        sel_app2btn.grid(row=1, column=2)
        sel_app3btn = tk.Button(self, text="Select", command=self.sel_app3_func)
        sel_app3btn.grid(row=2, column=2)
        sel_app4tn = tk.Button(self, text="Select", command=self.sel_app4_func)
        sel_app4tn.grid(row=3, column=2)
        sel_app5tn = tk.Button(self, text="Select", command=self.sel_app5_func)
        sel_app5tn.grid(row=4, column=2)
        reload_appbtn = tk.Button(self, text="Reload", command=self.reload_app_func)
        reload_appbtn.grid(row=5, column=2)


class HelpForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        backbtn = tk.Button(self, text="Back", command=lambda: controller.show_frame("DashboardForm"))
        backbtn.grid()

        help_data = cs.read_help_file()
        text = tk.Text(self)
        text.insert(tk.END, help_data)
        text.grid(row=2, column=0)


class StartApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.app_data = {
            "Username": tk.StringVar(),
            "password": tk.StringVar(),
            "in_file": tk.StringVar(),
            "app_1": tk.StringVar(),
            "app_2": tk.StringVar(),
            "app_3": tk.StringVar(),
            "app_4": tk.StringVar(),
            "app_5": tk.StringVar(),
        }

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginForm, DashboardForm, SettingsForm, HelpForm, RegisterForm):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginForm")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


if __name__ == "__main__":
    app = StartApp()
    app.title("My app")
    app.mainloop()
