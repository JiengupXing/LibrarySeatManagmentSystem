#!/usr/bin/env python
from tkinter import *
from views.formmanage import FormManageImport
from views.formmain import FormMainStudent, FormMainAdministor
from views.formlogin import FormLogin
from views.splash import SplashScreen
from tkinter import font
class App:

    def __init__(self):
        self.master = Tk()
        self.currentWindow = FormLogin(self.master)

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    SplashScreen()
    app = App()
    app.run()