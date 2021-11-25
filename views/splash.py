from tkinter import *
from tkinter import font
import time

class SplashScreen():

	def __init__(self):
		self.master = Tk()
		self.master.title("Loader Anim")
		self.master.geometry("350x200+600+200")
		self.master.resizable(0,0)
		self.master.overrideredirect(1)
		self.someFont = font.Font(family='Ubuntu', size=25, weight='bold')
		self.empty_canvas = Canvas(self.master,width = 300,height=150,highlightthickness=0)
		self.empty_canvas.grid(row = 1,column = 1)
		self.lab1 = Label(self.empty_canvas,text = "HZAU LIBRARY",font = font.Font(family='Ubuntu', size=30, weight='bold'),fg="#2b5876")
		self.lab1.grid(row = 1,column=1)
		self.lab2 = Label(self.empty_canvas,text = "seat management system",font = font.Font(size=20),fg="#2b5876")
		self.lab2.grid(row = 2,column=1)
		self.loader_canvas = Canvas(self.master,width = 300,height=20,highlightthickness=0)
		self.loader_canvas.grid(row = 2,column = 1)
		loader_value = 10

		while loader_value < 400:
			self.loader = self.loader_canvas.create_rectangle(20,10,loader_value,2,fill = "#708090",width=0)
			loader_value += 10
			time.sleep(0.1)
			self.master.update()

		time.sleep(1)
		self.master.destroy()
