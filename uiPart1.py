from tkinter import *
from tkinter import messagebox
import createSettings as cs


class LoginFrame(Frame):



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
                    # TODO go to dashboard page and hide this one
                    print("on DashboardForm1")
                else:
                    messagebox.showerror("Login error", "Incorrect Credentials")
                    input_uname = self.entry_username.delete(0, END)
                    input_pwd  = self.entry_password.delete(0, END)

    
    def register_func(self):
        print("in register_func")
        '''
        uname_val = self.entry_uname.get_text()
        pwd_val  = self.entry_pwd.get_text()
        in_file = uname_val+".json"

        ciphertext_input = cs.encrypt(pwd_val)

        if cs.file_existence(in_file) == False:
            print("file does not exist so write settings")
            if cs.checkEmpty(uname_val) == False and cs.checkEmpty(pwd_val) == False:
                created_settings_file = cs.write_settings(uname_val, ciphertext_input, "abc", "abc", "abc", "abc", "abc")
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
        '''

    
    def display_signup(self):
        signup_page = Toplevel()
        signup_page.title("Sign Up")
        signup_page.geometry("550x350+185+175")
        title_label = Label(signup_page ,text="Sign Up",font=("arial",20,"bold"),fg="blue").place(x=230,y=50)

	    #label for username
        uname_label = Label(signup_page ,text="Enter username",font=("arial",13,"bold"),fg="black").place(x=130,y=100)
        entry_username_signup = Entry(signup_page,width=15,bg="white").place(x=330,y=100)
        pswd_label =  Label(signup_page ,text="Enter password",font=("arial",13,"bold"),fg="black").place(x=130,y=150) 
        entry_pswd_signup = Entry(signup_page,width=15,bg="white").place(x=330,y=150)
        
        registerbtn_signup = Button(signup_page, text="Register", command=self.register_func).place(x=330,y=180)
        
    
    
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.loginbtn = Button(self, text="Login", command=self.login_func)
        self.loginbtn.grid(columnspan=2)

        self.registerbtn = Button(self, text="Register", command=self.display_signup)
        self.registerbtn.grid(columnspan=2)

        self.pack()



root = Tk()
lf = LoginFrame(root)
root.mainloop()