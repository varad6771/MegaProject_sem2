import tkinter as tk
import createSettings as cs
import detection as det

from tkinter import messagebox
from tkinter import filedialog
from tkinter import font as tkfont
from tkinter import ttk


class LoginForm(tk.Frame):

    def login_func(self):
        input_uname = self.entry_username.get()
        input_pwd = self.entry_password.get()

        in_file = input_uname + ".json"
        path = cs.get_path()
        in_file = path + "/" + input_uname + "/" + in_file
        if cs.file_existence(in_file) is False:
            print("file does not exist so login fail")
            messagebox.showerror("Login Fail", "User does not Exist")
            self.entry_username.delete(0, tk.END)
            self.entry_password.delete(0, tk.END)
        else:
            self.controller.app_data["Username"].set(input_uname)
            self.controller.app_data["in_file"].set(in_file)
            self.controller.app_data["password"].set(input_pwd)
            updated_path_val = path + "/" + input_uname
            self.controller.app_data["doc_path"].set(updated_path_val)

            input_data = cs.read_settings(in_file)
            for data_file in input_data['Settings']:

                red_pwd = data_file['password']
                red_unm = data_file['name']
                if cs.check_unm(red_unm, input_uname) is True and cs.check_pswd(red_pwd, input_pwd) is True:
                    print("login success")
                    self.controller.app_data["speciality"].set(data_file['speciality'])
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

        self.label_username = ttk.Label(self, text="Username")
        self.label_password = ttk.Label(self, text="Password")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.place(x=100, y=120)
        self.label_password.place(x=100, y=170)
        self.entry_username.place(x=180, y=120)
        self.entry_password.place(x=180, y=170)

        loginbtn = ttk.Button(self, text="Login", command=self.login_func)
        loginbtn.place(x=80, y=220)
        registerbtn = ttk.Button(self, text="Registration", command=lambda: controller.show_frame("RegisterForm"))
        registerbtn.place(x=180, y=220)

        clearbtn = ttk.Button(self, text="Clear", command=self.clear_func)
        clearbtn.place(x=280, y=220)

        self.pack()


class RegisterForm(tk.Frame):

    def register_func(self):
        print("in register_func")
        uname_val = self.entry_username.get()
        pwd_val = self.entry_password.get()
        pwd_re_val = self.entry_password_reenter.get()
        speciality_val = self.entry_speciality.get()

        if cs.check_empty(pwd_re_val) is True:
            messagebox.showerror("Empty Credentials", "Please fill all the fields")
        elif pwd_re_val != pwd_val:
            messagebox.showerror("Password do not match", "Please enter same password")
        else:
            in_file = uname_val + ".json"
            ciphertext_input = cs.encrypt(pwd_val)
            path = cs.create_dir(uname_val, 'abc', True)
            print("path register = ", path)
            in_file = path + "/" + in_file
            if cs.file_existence(in_file) is False:
                print("file does not exist so write settings")
                if cs.check_empty(uname_val) is False and cs.check_empty(pwd_val) is False:
                    created_settings_file = cs.write_doc_settings(uname_val, ciphertext_input, speciality_val, path)
                    print("register successful file created  " + created_settings_file)
                    messagebox.showinfo("Register Succesful", "Please set app preferences in settings")
                    self.entry_username.delete(0, tk.END)
                    self.entry_password.delete(0, tk.END)
                    self.entry_password_reenter.delete(0, tk.END)
                    self.entry_speciality.delete(0, tk.END)
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
        self.label_password_reenter = tk.Label(self, text="Re-enter Password")
        self.label_speciality = tk.Label(self, text="Speciality")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password_reenter = tk.Entry(self, show="*")
        self.entry_speciality = tk.Entry(self)

        self.label_username.place(x=50, y=50)
        self.label_password.place(x=50, y=100)
        self.label_password_reenter.place(x=50, y=150)
        self.label_speciality.place(x=50, y=200)
        self.entry_username.place(x=180, y=50)
        self.entry_password.place(x=180, y=100)
        self.entry_password_reenter.place(x=180, y=150)
        self.entry_speciality.place(x=180, y=200)

        registerbtn = ttk.Button(self, text="Register", command=self.register_func)
        registerbtn.place(x=200, y=250)

        backbtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame("LoginForm"))
        backbtn.place(x=100, y=250)


class DashboardForm(tk.Frame):

    def runapp_func(self):
        print("In the run app func")
        app1_dbf = self.controller.app_data["app_1"].get()
        app2_dbf = self.controller.app_data["app_2"].get()
        app3_dbf = self.controller.app_data["app_3"].get()
        app4_dbf = self.controller.app_data["app_4"].get()
        app5_dbf = self.controller.app_data["app_5"].get()
        # det.get_user_prefs(app1_dbf, app2_dbf, app3_dbf, app4_dbf, app5_dbf)
        # det.detect()

    def logout_func(self):
        print(" in logout function")
        self.controller.app_data["Username"].set(" ")
        self.controller.app_data["password"].set(" ")
        self.controller.app_data["speciality"].set(" ")
        self.controller.app_data["in_file"].set(" ")
        self.controller.app_data["doc_path"].set(" ")
        self.controller.app_data["app_1"].set(" ")
        self.controller.app_data["app_2"].set(" ")
        self.controller.app_data["app_3"].set(" ")
        self.controller.app_data["app_4"].set(" ")
        self.controller.app_data["app_5"].set(" ")
        self.controller.app_data["in_file_p"].set(" ")
        self.controller.app_data["patient_name"].set(" ")
        self.controller.app_data["patient_path"].set(" ")
        self.controller.show_frame("LoginForm")

    def selectp_func(self):
        global var
        var = tk.StringVar(self)
        var.set("Select Patient")

        path = self.controller.app_data["doc_path"].get()
        # BUG toget the list in dict or list in correct format
        plist = cs.read_plist_file(path)
        print(plist)
        options = ttk.OptionMenu(self, var, *plist)
        
        options.place(x=230, y=230)

    def selectopt_func(self):
        print("value is", var.get())
        self.controller.app_data["ch_patient"].set(var.get())

    def modview_func(self):
        if cs.check_empty(var.get()) is False:
            self.controller.show_frame("ModViewForm")
        else:
            messagebox.showerror("Empty Field", "Please Select a Patient")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        select_patientbtn = ttk.Button(self, text="Choose Patient", command=self.selectp_func)
        select_patientbtn.place(x=160, y=240)

        selopttbtn = ttk.Button(self, text="Select", command=self.selectopt_func)
        selopttbtn.place(x=160, y=50)

        runappbtn = ttk.Button(self, text="Run app", command=self.runapp_func)
        runappbtn.place(x=160, y=100)

        settingsbtn = ttk.Button(self, text="Settings Page", command=lambda: controller.show_frame("SettingsForm"))
        settingsbtn.place(x=157, y=160)

        helpbtn = ttk.Button(self, text="Help Page", command=lambda: controller.show_frame("HelpForm"))
        helpbtn.place(x=160, y=220)

        logoutbtn = ttk.Button(self, text="Logout", command=self.logout_func)
        logoutbtn.place(x=160, y=280)

        modifyviewbtn = ttk.Button(self, text="Modify/View Patient", command=self.modview_func)
        modifyviewbtn.place(x=160, y=340)


class HelpForm(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        backbtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame("DashboardForm"))
        backbtn.grid()

        help_data = cs.read_help_file()
        text = tk.Text(self)
        text.insert(tk.END, help_data)
        text.grid(row=2, column=0)


class ModViewForm(tk.Frame):

    def sel_app1_func(self):
        global entry_app_var1
        self.entry_app1.delete(0, tk.END)
        entry_app_var1 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app1.insert(0, entry_app_var1)

    def sel_app2_func(self):
        global entry_app_var2
        self.entry_app2.delete(0, tk.END)
        entry_app_var2 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app2.insert(0, entry_app_var2)

    def sel_app3_func(self):
        global entry_app_var3
        self.entry_app3.delete(0, tk.END)
        entry_app_var3 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app3.insert(0, entry_app_var3)

    def sel_app4_func(self):
        global entry_app_var4
        self.entry_app4.delete(0, tk.END)
        entry_app_var4 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app4.insert(0, entry_app_var4)

    def sel_app5_func(self):
        global entry_app_var5
        self.entry_app5.delete(0, tk.END)
        entry_app_var5 = filedialog.askopenfilename(filetypes=[("All files", "*")])
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
            patient_name = self.controller.app_data["ch_patient"].get()
            p_path = self.controller.app_data["doc_path"].get()
            path = p_path + "/" + patient_name

            if cs.check_empty(entry_app_var1) is False and cs.check_empty(entry_app_var2) is False and cs.check_empty(
                    entry_app_var3) is False and cs.check_empty(entry_app_var4) is False and cs.check_empty(
                    entry_app_var5) is False:
                patients_setting_file = cs.write_patient_settings(patient_name, entry_app_var1, entry_app_var2,
                                                                  entry_app_var3, entry_app_var4, entry_app_var5, path)
            else:
                messagebox.showerror("Empty Fields", "Please fill all the fields")

            if cs.file_existence(patients_setting_file) is True:
                self.controller.app_data["app_1"].set(entry_app_var1)
                self.controller.app_data["app_2"].set(entry_app_var2)
                self.controller.app_data["app_3"].set(entry_app_var3)
                self.controller.app_data["app_4"].set(entry_app_var4)
                self.controller.app_data["app_5"].set(entry_app_var5)

                print("settings saved file   " + patients_setting_file)
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

        self.controller.app_data["app_1"].set("abc")
        self.controller.app_data["app_2"].set("abc")
        self.controller.app_data["app_3"].set("abc")
        self.controller.app_data["app_4"].set("abc")
        self.controller.app_data["app_5"].set("abc")

        p_name = self.controller.app_data["ch_patient"].get()
        p_path = self.controller.app_data["doc_path"].get()
        in_file_patient = p_path + "/" + p_name + "/" + p_name + ".json"

        print("reset file name " + in_file_patient)

        if cs.file_reset(in_file_patient) is True:
            messagebox.showinfo("Succesful Reset", "Settings Reseted!! Please enter new settings before logging out ")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed. Please try again")

    def reload_app_func(self):
        print("in reload func")
        self.label_patient_name.config(text=self.controller.app_data["ch_patient"].get())
        varchck = self.entry_app1.get()

        p_name = self.controller.app_data["ch_patient"].get()
        p_path = self.controller.app_data["doc_path"].get()
        in_file_p = p_path + "/" + p_name + "/" + p_name + ".json"

        print(in_file_p)

        input_data = cs.read_settings(in_file_p)
        for data_file in input_data['Settings']:
            if cs.check_empty(varchck) is True:
                self.entry_app1.insert(0, data_file['app1'])
                self.entry_app2.insert(0, data_file['app2'])
                self.entry_app3.insert(0, data_file['app3'])
                self.entry_app4.insert(0, data_file['app4'])
                self.entry_app5.insert(0, data_file['app5'])

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_app1 = tk.Label(self, text="Gesture Fist")
        self.label_app2 = tk.Label(self, text="Gesture two")
        self.label_app3 = tk.Label(self, text="Gesture three")
        self.label_app4 = tk.Label(self, text="Gesture four")
        self.label_app5 = tk.Label(self, text="Gesture five")
        self.label_pname = tk.Label(self, text="Patient Name")
        self.label_patient_name = tk.Label(self, text="val_uname")

        self.entry_app1 = tk.Entry(self)
        self.entry_app2 = tk.Entry(self)
        self.entry_app3 = tk.Entry(self)
        self.entry_app4 = tk.Entry(self)
        self.entry_app5 = tk.Entry(self)

        self.label_app1.place(x=30, y=30)
        self.label_app2.place(x=30, y=70)
        self.label_app3.place(x=30, y=110)
        self.label_app4.place(x=30, y=150)
        self.label_app5.place(x=30, y=190)
        self.label_pname.place(x=30, y=230)
        self.label_patient_name.place(x=150, y=230)

        self.entry_app1.place(x=120, y=30)
        self.entry_app2.place(x=120, y=70)
        self.entry_app3.place(x=120, y=110)
        self.entry_app4.place(x=120, y=150)
        self.entry_app5.place(x=120, y=190)

        sel_app1btn = ttk.Button(self, text="Select", command=self.sel_app1_func)
        sel_app1btn.place(x=290, y=30)
        sel_app2btn = ttk.Button(self, text="Select", command=self.sel_app2_func)
        sel_app2btn.place(x=290, y=70)
        sel_app3btn = ttk.Button(self, text="Select", command=self.sel_app3_func)
        sel_app3btn.place(x=290, y=110)
        sel_app4tn = ttk.Button(self, text="Select", command=self.sel_app4_func)
        sel_app4tn.place(x=290, y=150)
        sel_app5tn = ttk.Button(self, text="Select", command=self.sel_app5_func)
        sel_app5tn.place(x=290, y=190)

        resetbtn = ttk.Button(self, text="Reset", command=self.reset_func)
        resetbtn.place(x=70, y=330)

        savebtn = ttk.Button(self, text="Save", command=self.save_func)
        savebtn.place(x=170, y=330)

        backbtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame("SettingsForm"))
        backbtn.place(x=270, y=330)

        reload_appbtn = ttk.Button(self, text="Reload", command=self.reload_app_func)
        reload_appbtn.place(x=290, y=230)


class SettingsForm(tk.Frame):

    def save_func(self):
        print("in save_func")

        global entry_passwd_var6
        global entry_speciality_val

        entry_passwd_var6 = self.entry_password_settingsui.get()
        entry_speciality_val = self.entry_speciality_settingsui.get()

        input_uname = self.controller.app_data["Username"].get()
        input_pwd = self.controller.app_data["password"].get()
        speciality_val = self.controller.app_data["speciality"].get()
        path_val = self.controller.app_data["doc_path"].get()

        if cs.check_empty(entry_passwd_var6) is True:
            entry_passwd_var6 = input_pwd
        else:
            entry_passwd_var6 = self.entry_password_settingsui.get()

        if cs.check_empty(entry_speciality_val) is True:
            entry_speciality_val = speciality_val
        else:
            entry_speciality_val = self.entry_speciality_settingsui.get()

        ciphertext_input = cs.encrypt(entry_passwd_var6)
        created_settings_file = cs.write_doc_settings(input_uname, ciphertext_input, entry_speciality_val, path_val)

        if cs.file_existence(created_settings_file) is True:
            self.controller.app_data["password"].set(entry_passwd_var6)
            self.controller.app_data["speciality"].set(entry_speciality_val)

            print("settings saved file name   " + created_settings_file)
            messagebox.showinfo("Save Successful", "New Settings are Updated Successfully ")
        else:
            messagebox.showerror("Update Failed", "New Settings are not Updated!! Please try again later")

    def reset_func(self):
        print("in reset_func")

        self.entry_password_settingsui.delete(0, tk.END)
        self.entry_speciality_settingsui.delete(0, tk.END)

        in_file = self.controller.app_data["in_file"].get()
        print("reset file name " + in_file)
        # path_val = self.controller.app_data["doc_path"].get()

        # BUG reset also removes folder instead of just file
        if cs.file_reset(in_file) is True:
            messagebox.showinfo("Succesful Reset", "Settings Reseted!! Please enter new settings before logging out ")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed. Please try again")

    def reload_app_func(self):
        self.label_uname_display.config(text=self.controller.app_data["Username"].get())
        self.entry_speciality_settingsui.insert(0, self.controller.app_data["speciality"].get())

    def addpatient_func(self):
        print("in add patient")
        patientnameval = self.entry_patient_name.get()

        if cs.check_empty(patientnameval) is False:
            doc_uname = self.controller.app_data["Username"].get()
            path_val = self.controller.app_data["doc_path"].get()

            patient_dir = cs.create_dir(doc_uname, patientnameval, False)
            print("patient dir is ", patient_dir)
            patients_file = cs.write_patient_settings(patientnameval, "abc", "abc", "abc", "abc", "abc", patient_dir)
            plist_fname = cs.write_plist_file(patientnameval, path_val)

            if cs.file_existence(plist_fname):
                print("patient added to file")
                self.controller.app_data["patient_name"].set(patientnameval)
                self.controller.app_data["patient_path"].set(patient_dir)
                self.controller.app_data["in_file_p"].set(patients_file)
                self.controller.show_frame("PatientsForm")
            else:
                print("patient name not added to list")
        else:
            messagebox.showerror("Empty Field", "Please fill the patients name ")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_patient_name = tk.Label(self, text="Patient Name")
        self.label_uname = tk.Label(self, text="Username")
        self.label_uname_display = tk.Label(self, text="val_uname")
        self.label_password_settingsui = tk.Label(self, text="Password")
        self.label_speciality_settingsui = tk.Label(self, text="Speciality")

        self.entry_speciality_settingsui = tk.Entry(self)
        self.entry_patient_name = tk.Entry(self)
        self.entry_password_settingsui = tk.Entry(self, show="*")

        self.label_patient_name.place(x=30, y=30)
        self.label_uname.place(x=30, y=230)
        self.label_uname_display.place(x=150, y=230)
        self.label_speciality_settingsui.place(x=30, y=270)
        self.label_password_settingsui.place(x=30, y=300)

        self.entry_patient_name.place(x=120, y=30)
        self.entry_speciality_settingsui.place(x=120, y=270)
        self.entry_password_settingsui.place(x=120, y=300)

        addpatientbtn = ttk.Button(self, text="Add Patient", command=self.addpatient_func)
        addpatientbtn.place(x=70, y=90)

        resetbtn = ttk.Button(self, text="Reset", command=self.reset_func)
        resetbtn.place(x=70, y=330)

        # changes in savefunc
        savebtn = ttk.Button(self, text="Save", command=self.save_func)
        savebtn.place(x=170, y=330)

        backbtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame("DashboardForm"))
        backbtn.place(x=270, y=330)

        reload_appbtn = ttk.Button(self, text="Reload", command=self.reload_app_func)
        reload_appbtn.place(x=290, y=230)


class PatientsForm(tk.Frame):

    def sel_app1_func(self):
        global entry_app_var1
        self.entry_app1.delete(0, tk.END)
        entry_app_var1 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app1.insert(0, entry_app_var1)

    def sel_app2_func(self):
        global entry_app_var2
        self.entry_app2.delete(0, tk.END)
        entry_app_var2 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app2.insert(0, entry_app_var2)

    def sel_app3_func(self):
        global entry_app_var3
        self.entry_app3.delete(0, tk.END)
        entry_app_var3 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app3.insert(0, entry_app_var3)

    def sel_app4_func(self):
        global entry_app_var4
        self.entry_app4.delete(0, tk.END)
        entry_app_var4 = filedialog.askopenfilename(filetypes=[("All files", "*")])
        self.entry_app4.insert(0, entry_app_var4)

    def sel_app5_func(self):
        global entry_app_var5
        self.entry_app5.delete(0, tk.END)
        entry_app_var5 = filedialog.askopenfilename(filetypes=[("All files", "*")])
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
            path = self.controller.app_data["patient_path"].get()
            patient_name = self.controller.app_data["patient_name"].get()
            if cs.check_empty(entry_app_var1) is False and cs.check_empty(entry_app_var2) is False and cs.check_empty(
                    entry_app_var3) is False and cs.check_empty(entry_app_var4) is False and cs.check_empty(
                    entry_app_var5) is False:
                patients_setting_file = cs.write_patient_settings(patient_name, entry_app_var1, entry_app_var2,
                                                                  entry_app_var3, entry_app_var4, entry_app_var5, path)
            else:
                messagebox.showerror("Empty Fields", "Please fill all the fields")

            if cs.file_existence(patients_setting_file) is True:
                print("settings saved file   " + patients_setting_file)
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

        in_file_patient = self.controller.app_data["in_file_p"].get()
        print("reset file name " + in_file_patient)

        if cs.file_reset(in_file_patient) is True:
            messagebox.showinfo("Succesful Reset", "Settings Reseted!! Please enter new settings before logging out ")
        else:
            messagebox.showerror("Reset Fail", "Settings Reset Failed. Please try again")

    def reload_app_func(self):
        print("in reload func")
        self.label_patient_name.config(text=self.controller.app_data["patient_name"].get())
        varchck = self.entry_app1.get()

        in_file_p = self.controller.app_data["in_file_p"].get()
        input_data = cs.read_settings(in_file_p)
        for data_file in input_data['Settings']:
            if cs.check_empty(varchck) is True:
                self.entry_app1.insert(0, data_file['app1'])
                self.entry_app2.insert(0, data_file['app2'])
                self.entry_app3.insert(0, data_file['app3'])
                self.entry_app4.insert(0, data_file['app4'])
                self.entry_app5.insert(0, data_file['app5'])

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.label_app1 = tk.Label(self, text="Gesture Fist")
        self.label_app2 = tk.Label(self, text="Gesture two")
        self.label_app3 = tk.Label(self, text="Gesture three")
        self.label_app4 = tk.Label(self, text="Gesture four")
        self.label_app5 = tk.Label(self, text="Gesture five")
        self.label_pname = tk.Label(self, text="Patient Name")
        self.label_patient_name = tk.Label(self, text="val_uname")

        self.entry_app1 = tk.Entry(self)
        self.entry_app2 = tk.Entry(self)
        self.entry_app3 = tk.Entry(self)
        self.entry_app4 = tk.Entry(self)
        self.entry_app5 = tk.Entry(self)

        self.label_app1.place(x=30, y=30)
        self.label_app2.place(x=30, y=70)
        self.label_app3.place(x=30, y=110)
        self.label_app4.place(x=30, y=150)
        self.label_app5.place(x=30, y=190)
        self.label_pname.place(x=30, y=230)
        self.label_patient_name.place(x=150, y=230)

        self.entry_app1.place(x=120, y=30)
        self.entry_app2.place(x=120, y=70)
        self.entry_app3.place(x=120, y=110)
        self.entry_app4.place(x=120, y=150)
        self.entry_app5.place(x=120, y=190)

        sel_app1btn = ttk.Button(self, text="Select", command=self.sel_app1_func)
        sel_app1btn.place(x=290, y=30)
        sel_app2btn = ttk.Button(self, text="Select", command=self.sel_app2_func)
        sel_app2btn.place(x=290, y=70)
        sel_app3btn = ttk.Button(self, text="Select", command=self.sel_app3_func)
        sel_app3btn.place(x=290, y=110)
        sel_app4tn = ttk.Button(self, text="Select", command=self.sel_app4_func)
        sel_app4tn.place(x=290, y=150)
        sel_app5tn = ttk.Button(self, text="Select", command=self.sel_app5_func)
        sel_app5tn.place(x=290, y=190)

        resetbtn = ttk.Button(self, text="Reset", command=self.reset_func)
        resetbtn.place(x=70, y=330)

        savebtn = ttk.Button(self, text="Save", command=self.save_func)
        savebtn.place(x=170, y=330)

        backbtn = ttk.Button(self, text="Back", command=lambda: controller.show_frame("SettingsForm"))
        backbtn.place(x=270, y=330)

        reload_appbtn = ttk.Button(self, text="Reload", command=self.reload_app_func)
        reload_appbtn.place(x=290, y=230)


class StartApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.app_data = {
            "Username": tk.StringVar(),
            "password": tk.StringVar(),
            "speciality": tk.StringVar(),
            "in_file": tk.StringVar(),
            "doc_path": tk.StringVar(),
            "app_1": tk.StringVar(),
            "app_2": tk.StringVar(),
            "app_3": tk.StringVar(),
            "app_4": tk.StringVar(),
            "app_5": tk.StringVar(),
            "in_file_p": tk.StringVar(),
            "patient_name": tk.StringVar(),
            "ch_patient": tk.StringVar(),
            "patient_path": tk.StringVar(),
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
        for F in (LoginForm, DashboardForm, SettingsForm, HelpForm, RegisterForm, PatientsForm, ModViewForm):
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
    app.title("Hand Gesture Recognition")
    app.geometry('500x500')
    app.mainloop()
