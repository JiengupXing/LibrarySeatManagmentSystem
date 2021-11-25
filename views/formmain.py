from tkinter import *
from tkinter import font
from tkinter import ttk
from tkinter import messagebox
from .form import Form
from PIL import Image, ImageTk
import pandas as pd

class FormMainStudent(Form):
    def __init__(self, master, userinfo):
        Form.__init__(self, master)
        self._initialize(master, userinfo)
        self._initialize_view(master)

    def _initialize(self, master, userinfo):
        self.info = userinfo
        self.img_seat_takable = PhotoImage(file = "img/seat_takable.png")
        self.img_seat_taken = PhotoImage(file = "img/seat_taken.png")

    def _initialize_view(self, master):
        #row1-part
        self.master.title("Student Client")
        self.fra_left = Frame(master)
        self.information_lab = Label(self.fra_left, text = "Imformation", font = font.Font(size = 25, weight = "bold"))
        #.encode('latin-1').decode('gbk')
        infostr = "user_name: " + str(self.info[0][0]) + "\n" + "name: " + self.info[0][2].encode('latin-1').decode('gbk') + "\n" + "sex: " + self.info[0][3] + "\n" + "Institute: " + self.info[0][8] + "\n" + "Class: " + self.info[0][7] + self.info[0][6]
        self.info_lab = Label(self.fra_left, font = font.Font(size = 15), text = infostr)
        self.btn_logout = Button(self.fra_left, text = "logout", command = self._on_buttonclick_logout)
        self.fra_right = Frame(master)
        self.floor_lab = Label(self.fra_right, text = "Floors", font = font.Font(size = 15, weight = "bold"))
        floors = ("floor1", "floor2")
        self.cmb_floor = ttk.Combobox(self.fra_right, state = "readonly", values = floors)
        self.room_lab = Label(self.fra_right, text = "Rooms", font = font.Font(size = 15, weight = "bold"))
        rooms = ("01", "02", "03")
        self.cmb_room = ttk.Combobox(self.fra_right, state = "readonly", values = rooms)
        self.information_lab.grid(row = 1, column = 1)
        self.info_lab.grid(row = 2, column = 1)
        self.btn_logout.grid(row = 3, column = 1)
        self.fra_left.grid(row = 1, column = 1)
        self.floor_lab.grid(row = 1, column = 1)
        self.room_lab.grid(row = 1, column = 2)
        self.cmb_floor.grid(row = 2, column = 1)
        self.cmb_room.grid(row = 2, column = 2)
        self.fra_right.grid(row = 1, column = 2)
        
        self.cmb_floor.bind("<<ComboboxSelected>>", self._on_combobox_selected)
        self.cmb_room.bind("<<ComboboxSelected>>", self._on_combobox_selected)

        self.fra_seats = Frame(master)
        self.seats_btn_list = []
        for i in range(4):
            seats_btn_row = []
            for j in range(5):
                btn = Button(self.fra_seats, text = str(i+1) + "-" + str(j+1), image = self.img_seat_takable)
                btn.config(command = lambda BTN = btn : self._on_button_clicked(BTN), cursor = "hand2")
                btn.grid(row = i+1, column = j+1)
                seats_btn_row.append(btn)
            self.seats_btn_list.append(seats_btn_row)
        self.fra_seats.grid(row = 2, column = 2)

    def show_room_state(self, floor, room):
        #SELECT FROM DATABASE
        room_id = "'" + floor[-1] + room + "'"
        query_statu_sql = "select STstatus from Seats where Rid = " + room_id
        try:
            from dboperate.db import Db
            db = Db()
            selected_seats_status = db.query(query_statu_sql)
            #print(selected_seats_status)
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
        for i in range(4):
            for j in range(5):
                idx = i*5+j
                if selected_seats_status[idx][0]:
                    self.seats_btn_list[i][j]["image"] = self.img_seat_taken
                    self.seats_btn_list[i][j]["state"] = "disable"
                else:
                    self.seats_btn_list[i][j]["image"] = self.img_seat_takable
                    self.seats_btn_list[i][j]["state"] = "normal"
        self.frash()
    
    

    def _on_combobox_selected(self, event = None):
        floor = self.cmb_floor.get()
        room = self.cmb_room.get()
        if room == "" or floor == "":
            return
        self.show_room_state(floor = floor, room = room)
    
    def _on_button_clicked(self, btn):
        floor = self.cmb_floor.get()
        room = self.cmb_room.get()
        pos = btn["text"]
        if floor == "" or room == "":
            messagebox.showerror("ERROR!", "please select floor and room")
        else:
            check = messagebox.askyesno(title = "Make Sure", message = "Are you sure to take this\n" + pos  + " seat\nin ROOM " + floor[-1] + room + " of " + floor.upper() + "?")
            if check == True:
                self.close()
                self.take_a_seat(pos = pos, floor = floor, room = room)
            else:
                print("cancel")

    def take_a_seat(self, pos, floor, room):
        Rid = "'" + floor[-1] + room + "'"
        seat_num = (int(pos[0])-1)*5 + (int(pos[2])-1) + 1
        STid = "'0"
        if seat_num < 10:
            STid += "0" + str(seat_num) + "'"
        else:
            STid += str(seat_num) + "'"
        #UPDATE INTO DATABASE
        update_Seats_sql = "update Seats set STstatus = 1 where Rid = " + Rid + " and " + "STid = " + STid
        #INSERT INTO RECOEDS
        from dboperate.db import Db
        import sys
        import time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        RCDid = current_time[0:4] + current_time[5:7] + current_time[8:10]
        current_time = "'" + current_time + "'"
        num = 0
        while True:
            tempid = "'" + RCDid + str("%02d" % num) + "'"
            db = Db()
            if not db.query("select * from Records where RCDid = " + tempid):
                break
            else:
                num += 1
        RCDid = tempid
        insert_Records_sql = "insert into Records values (" + RCDid + ", " + str(self.info[0][0]) + ", " + Rid + ", " + STid + ", " + current_time + ", " + "'student', " + "'take')"
        try:
            db = Db()
            db.operate(insert_Records_sql)
            db.operate(update_Seats_sql)
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
        from .formstudy import FormStudy
        FormStudy(Tk(), [pos, floor, room], self.info)
    
    def _on_buttonclick_logout(self):
        self.close()




class FormMainAdministor(Form):
    def __init__(self, master, userinfo):
        Form.__init__(self, master)
        self._initialize(master, userinfo)
        self._initialize_view(master)

    def _initialize(self, master, userinfo):
        self.info = userinfo 

    def _initialize_view(self, master):
        #row1-part
        self.master.title("Administor Client")
        self.fra_left = Frame(master)
        self.information_lab = Label(self.fra_left, text = "Imformation", font = font.Font(size = 25, weight = "bold"))
        infostr = "user_name: " + str(self.info[0][0]) + "\n" + "name: " + self.info[0][2].encode('latin-1').decode('gbk')
        self.info_lab = Label(self.fra_left, font = font.Font(size = 15), text = infostr)
        self.btn_logout = Button(self.fra_left, text = "logout", command = self._onbuttonclick_logout)
        self.fra_right = Frame(master)
        self.btn_import = Button(self.fra_right, text = "import a user", cursor = "hand2", command = self._on_buttonclick_import)
        self.btn_query = Button(self.fra_right, text = "query all records", cursor = "hand2", command = self._on_buttonclick_query)
        self.btn_lock = Button(self.fra_right, text = "lock a seat", cursor = "hand2", command = self._on_buttonclick_lock)
        self.btn_statics = Button(self.fra_right, text = "statics", cursor = "hand2", command = self._on_buttonclick_statics)
        self.information_lab.grid(row = 1, column = 1)
        self.info_lab.grid(row = 2, column = 1)
        self.btn_logout.grid(row = 3, column = 1)
        self.btn_import.grid(row = 1, column = 1)
        self.btn_query.grid(row = 2, column = 1)
        self.btn_lock.grid(row = 3, column = 1)
        self.btn_statics.grid(row = 4, column = 1)
        self.fra_left.grid(row = 1, column = 1)
        self.fra_right.grid(row = 1, column = 2)

    def _on_buttonclick_import(self):
        self.close()
        from .formmanage import FormManageImport
        FormManageImport(Tk(), self.info)
    
    def _on_buttonclick_query(self):
        self.close()
        from .formmanage import FormManageQuery
        FormManageQuery(Tk(), self.info)
    
    def _on_buttonclick_lock(self):
        self.close()
        from .formmanage import FormManageLock
        FormManageLock(Tk(), self.info)

    def _on_buttonclick_statics(self):
        self.close()
        from .formmanage import FormManageStatics
        FormManageStatics(Tk(), self.info)

    def _onbuttonclick_logout(self):
        self.close()