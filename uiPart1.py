import tkinter as tk  
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font  as tkfont
import createSettings as cs

# TODO: to set val of set settings in SettingsForm entry and labels
class LoginForm(tk.Frame):

    def login_func(self):
        # print("Clicked")
        input_uname = self.entry_username.get()
        input_pwd = self.entry_password.get()


        in_file = input_uname+".json"

        if cs.file_existence(in_file) == False:
            print("file does not exist so login fail")
            messagebox.showerror("Login Fail", "User does not Exist")
            input_uname = self.entry_username.delete(0, END)
            input_pwd  = self.entry_password.delete(0, END)
        else:
            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:

                red_pwd = data_file['password']
                red_unm = data_file['name']
                if cs.checkUnm(red_unm, input_uname) == True and cs.checkPwd(red_pwd, input_pwd) == True:
                    print("login success")
                    self.controller.show_frame("DashboardForm")
                    cs.set_uname(input_uname)
                    print("on DashboardForm1")
                else:
                    messagebox.showerror("Login error", "Incorrect Credentials")
                    input_uname = self.entry_username.delete(0, END)
                    input_pwd  = self.entry_password.delete(0, END)

    def register_func(self):
        print("in register_func")
        uname_val = self.entry_username.get()
        pwd_val  = self.entry_password.get()
        in_file = uname_val+".json"

        ciphertext_input = cs.encrypt(pwd_val)

        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            if cs.checkEmpty(uname_val) == False and cs.checkEmpty(pwd_val) == False:
                created_settings_file = cs.write_settings(uname_val, ciphertext_input, "abc", "abc", "abc", "abc", "abc")
                print("register successful file created  "+created_settings_file)
                messagebox.showinfo("Register Succesful", "Please set app preferences in settings")
                uname_val = self.entry_username.delete(0, END)
                pwd_val  = self.entry_password.delete(0, END)
            else:
                messagebox.showerror("Empty Credentials","Credential cannot be empty!! Please fill all the fields")
        else:
            input_data = cs.read_settings(in_file)
            for settings_data_file in input_data['Settings']:
                if settings_data_file['name'] == uname_val:
                    print("data exist! you cannot re-register")
                    messagebox.showerror("Error","User Already Exists!! You cannot Re-Register")
                    break

    def clear_func(self):
        print("in clear func")

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
        loginbtn.grid(row=2,column=0)

        registerbtn = tk.Button(self, text="Register", command=self.register_func)
        registerbtn.grid(row=2,column=1)

        clearbtn = tk.Button(self, text="Clear", command=self.clear_func)
        clearbtn.grid(row=2,column=2)

        self.pack()

class DashboardForm(tk.Frame):

    def runapp_func(self):
        print("In the run app func")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        runappbtn = tk.Button(self, text="Run app", command=self.runapp_func)
        runappbtn.grid(row=1,column=0)

        settingsbtn = tk.Button(self, text="Settings Page", command=lambda: controller.show_frame("SettingsForm"))
        settingsbtn.grid(row=1,column=1)
        
class SettingsForm(tk.Frame):

    def sel_app1_func(self):
        global entry_app_var1
        entry_app_var1 = filedialog.askopenfilename(filetypes=[("JPEG file","*.jpg")])
        self.entry_app1.insert(0, entry_app_var1)

    def sel_app2_func(self):
        global entry_app_var2
        entry_app_var2 = filedialog.askopenfilename(filetypes=[("JPEG file","*.jpg")])
        self.entry_app2.insert(0,entry_app_var2)

    def sel_app3_func(self):
        global entry_app_var3
        entry_app_var3 = filedialog.askopenfilename(filetypes=[("JPEG file","*.jpg")])
        self.entry_app3.insert(0,entry_app_var3)
    
    def sel_app4_func(self):
        global entry_app_var4
        entry_app_var4 = filedialog.askopenfilename(filetypes=[("JPEG file","*.jpg")])
        self.entry_app4.insert(0,entry_app_var4)
    
    def sel_app5_func(self):
        global entry_app_var5
        entry_app_var5 = filedialog.askopenfilename(filetypes=[("JPEG file","*.jpg")])
        self.entry_app5.insert(0,entry_app_var5)

    def save_func(self):
        print("in save_func")
        global entry_passwd_var6
        entry_passwd_var6 = self.entry_password_settingsui.get()

        input_uname = cs.get_uname()
        input_pwd = cs.get_pwd()


        if cs.checkEmpty(entry_passwd_var6) == True:
            entry_passwd_var6 = input_pwd
        else:
            entry_passwd_var6 = self.entry_password_settingsui.get()

        if cs.checkEmpty(entry_app_var1) == False and cs.checkEmpty(entry_app_var2) == False and cs.checkEmpty(entry_app_var3) == False and cs.checkEmpty(entry_app_var4) == False and cs.checkEmpty(entry_app_var5) == False:
            ciphertext_input = cs.encrypt(entry_passwd_var6)
            created_settings_file = cs.write_settings(input_uname, ciphertext_input, entry_app_var1, entry_app_var2, entry_app_var3, entry_app_var4, entry_app_var5)
        else:
            messagebox.showerror("Empty Fields","Please fill all the fields")


        if cs.file_existence(created_settings_file) == True:
            print("settings saved file name   "+created_settings_file)
            messagebox.showinfo("Save Succesful","New Settings are Updated Successfully ")
        else:
            messagebox.showerror("Update Failed","New Settings are not Updated!! Please try again later")

    def reset_func(self):
        print("in reset_func")
        #val1 = self.entry_app1.set_text("")
        #val2 = self.entry_app2.set_text("")
        #val3 = self.entry_app3.set_text("")
        #entry_passwd_var6 = self.entry_password_settingsui.set_text("")
        
        input_uname = cs.get_uname()
        in_file = input_uname+".json"
        print("reset file name "+in_file)
        
        if  cs.file_reset(in_file) == True:
            messagebox.showinfo("Succesful Reset", "Settings Reset Success!! Please enter new settings")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        val_uname = cs.get_uname()
        print("val_uname "+val_uname)
        self.label_app1 = tk.Label(self, text="Application 1")
        self.label_app2 = tk.Label(self, text="Application 2")
        self.label_app3 = tk.Label(self, text="Application 3")
        self.label_app4 = tk.Label(self, text="Application 4")
        self.label_app5 = tk.Label(self, text="Application 5")
        self.label_uname = tk.Label(self, text="Uname")
        self.label_uname_display = tk.Label(self, textvariable=val_uname)
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
        self.label_uname_display.grid(row=5,column=1)
        self.label_password_settingsui.grid(row=6)

        self.entry_app1.grid(row=0, column=1)
        self.entry_app2.grid(row=1, column=1)
        self.entry_app3.grid(row=2, column=1)
        self.entry_app4.grid(row=3, column=1)
        self.entry_app5.grid(row=4, column=1)
        self.entry_password_settingsui.grid(row=6, column=1)

        resetbtn = tk.Button(self, text="Reset", command=self.reset_func)
        resetbtn.grid(row=7,column=0)

        savebtn = tk.Button(self, text="Save", command=self.save_func)
        savebtn.grid(row=7,column=1)

        backbtn = tk.Button(self, text="Back", command=lambda: controller.show_frame("DashboardForm"))
        backbtn.grid(row=7,column=2)

        sel_app1btn = tk.Button(self, text="Select", command=self.sel_app1_func)
        sel_app1btn.grid(row=0,column=2)
        sel_app2btn = tk.Button(self, text="Select", command=self.sel_app2_func)
        sel_app2btn.grid(row=1,column=2)
        sel_app3btn = tk.Button(self, text="Select", command=self.sel_app3_func)
        sel_app3btn.grid(row=2,column=2)
        sel_app4tn = tk.Button(self, text="Select", command=self.sel_app4_func)
        sel_app4tn.grid(row=3,column=2)
        sel_app5tn = tk.Button(self, text="Select", command=self.sel_app5_func)
        sel_app5tn.grid(row=4,column=2)

        
        #label = tk.Label(self, text="This is Settings Page", font=controller.title_font)
        #label.pack(side="top", fill="x", pady=10)
        #button = tk.Button(self, text="Go to the start page",
        #                   command=lambda: controller.show_frame("LoginForm"))
        #button.pack()

class StartApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginForm, DashboardForm, SettingsForm):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginForm")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

if __name__ == "__main__":
    app = StartApp()
    app.mainloop()