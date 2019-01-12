import tkinter as tk  
from tkinter import messagebox
from tkinter import font  as tkfont
import createSettings as cs

# TODO: whereever uname is needed even for creating in_file we need to get uname 
#       i guess from cs as get Uname but it will mean read file each time of set var there once login successful
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

    def save_func(self):
        print("in save_func")
        
    def reset_func(self):
        print("in reset_func")
        print("input uname after login "+input_uname)
        #val1 = self.entry_app1.set_text("")
        #val2 = self.entry_app2.set_text("")
        #val3 = self.entry_app3.set_text("")
        #val4 = self.entry_password_settingsui.set_text("")
        
        reset_file_name = input_uname+".json"
        print("reset file name "+reset_file_name)
        
        if  cs.file_reset(reset_file_name) == True:
            messagebox.showinfo("Succesful Reset", "Settings Reset Success!! Please enter new settings")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        

        self.label_app1 = tk.Label(self, text="Application 1")
        self.label_app2 = tk.Label(self, text="Application 2")
        self.label_app3 = tk.Label(self, text="Application 3")
        self.label_app4 = tk.Label(self, text="Application 4")
        self.label_app5 = tk.Label(self, text="Application 5")
        self.label_uname = tk.Label(self, text="Uname")
        self.label_uname_display = tk.Label(self, text="need a var with unmae here")
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