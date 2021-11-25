from tkinter import *
from tkinter import messagebox
from .form import Form
from dboperate.db import Db
from PIL import Image, ImageTk
from time import sleep
from decimal import Decimal

class FormLogin(Form):

    def __init__(self, master):
        Form.__init__(self, master)
        self._initialize(master)
        self._initialize_view(master)

    def _initialize(self, master):
        self.username = StringVar()
        self.password = StringVar()
        self.friend = StringVar()
        self.message = StringVar()

    def _initialize_view(self, master):
        self.master.title("LSMS")
        self.master.geometry("350x340+600+300")
        self.master.resizable(0,0)
        hzauphoto = PhotoImage(file='img/hzaulogo.png')
        self.master.bind("<Return>", self._on_buttonlogin_clicked)
        self.fbImageFrame = Frame(master,width=350,height=30,bg='#E9EBEE')
        self.fblogo = Label(master, image=hzauphoto)
        self.fblogo.image = hzauphoto
        self.labelid = Label(master, text="Username",fg="#365899",bg="#E9EBEE")
        self.labelpass = Label(master, text="Password",fg="#365899",bg="#E9EBEE")

        self.entryid = Entry(master, textvariable=self.username)
        self.entrypass = Entry(master, show="*", textvariable=self.password)

        self.buttonlogin = Button(master,
                                  text="Login",
                                  command=self._on_buttonlogin_clicked,bg="#3B5970",fg="#F2FFFF",
                                  cursor="hand2",activebackground="#365899",activeforeground="#F2FFFF")

        self.fbImageFrame.grid(row=0, column=0)
        self.fblogo.grid(row=1, column=0,sticky=W,pady = 10,padx=90)

        self.labelid.grid(row=2, column=0,sticky=W,pady = 5,padx=90)
        self.entryid.grid(row=3, column=0,pady=5,ipady=5)

        self.labelpass.grid(row=4, column=0,sticky=W,pady = 5,padx=90)
        self.entrypass.grid(row=5, column=0,pady=5,ipady=5)
        self.buttonlogin.grid(row=6, column=0, columnspan=2,pady=5)

        self.login_state_info = Label(self.master,text="...",bg="#E9EBEE",fg="#365899")
        self.login_state_info.grid(row=7,column=0,pady=5,ipady=5)

    def _on_buttonlogin_clicked(self, event=None):
        self.login_state_info.config(text = "Logging you in...")
        self.master.update()
        sleep(1)
        
        user_name = (Decimal(self.username.get()),)
        password = (self.password.get(),)

        db = Db()
        #login success -> formmain
        try:
            query_librarians_id = "select Uid from Librarians"
            librarians_id_list = db.query(query_librarians_id)
            query_students_id = "select Uid from Students"
            students_id_list = db.query(query_students_id)
        except Exception as e:
            messagebox.showerror("ERROR!", e)
        if user_name in librarians_id_list:
            try:
                query_passwd = "select Upasswd from Librarians where Uid = " + str(user_name[0])
                correct_passwd = db.query(query_passwd)
            except Exception as e:
                messagebox.showerror("ERROR!", e)
            if password in correct_passwd:
                query_info = "select * from Librarians where Uid = " + str(user_name[0])
                try:
                    info = db.query(query_info)
                except Exception as e:
                    messagebox.showerror("ERROR!", e)
                self.close()
                #print(info)
                from .formmain import FormMainAdministor
                FormMainAdministor(Tk(), info)
            else:
                self.close()
                from .formloginfailure import FormLoginFailure
                FormLoginFailure(Tk())
        elif user_name in students_id_list:
            try:
                query_passwd = "select Upasswd from Students where Uid = " + str(user_name[0])
                correct_passwd = db.query(query_passwd)
            except Exception as e:
                messagebox.showerror("ERROR!", e)
            if password in correct_passwd:
                query_info = "select * from Students where Uid = " + str(user_name[0])
                try:
                    info = db.query(query_info)
                except Exception as e:
                    messagebox.showerror("ERROR!", e)
                self.close()
                from .formmain import FormMainStudent
                #print(info)
                FormMainStudent(Tk(), info)
            else:
                self.close()
                from .formloginfailure import FormLoginFailure
                FormLoginFailure(Tk())
        else:
            #login fail -> formloginfailure
            self.close()
            from .formloginfailure import FormLoginFailure
            FormLoginFailure(Tk())
        db.destroy()