from tkinter import *
from tkinter import font
from tkinter import messagebox
from .form import Form
from .formmain import FormMainStudent
import sys
import time

class FormStudy(Form):
    def __init__(self, master, seat_info, stu_info):
        Frame.__init__(self, master)
        self._initialize(master, seat_info, stu_info)
        self._initialize_view(master)

    def _initialize(self, master, seat_info, stu_info):
        self.info = seat_info
        self.stu = stu_info

    def _initialize_view(self, master):
        self.master.title("Study Mode")
        self.info_lb = Label(master, text = "YOU ARE TAKING THE SEAT", font = font.Font(size = 20), fg = "#365899")
        self.seatinfo = Label(master, text = self.info[0] + ", " + "room" + self.info[1][-1] + self.info[2] + ", " + self.info[1], font = font.Font(size = 15))
        self.lenth_lb = Label(master, text = "YOU HAVE BEEN STUDYING", font = font.Font(size = 20), fg = "#365899")
        self.total_time = Label(master, text = "0:00:00", font = font.Font(size = 50, weight = "bold"))
        self.empty_lb = Label(master)
        self.time_lb = Label(master, text = "current time: " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        self.leave_btn = Button(master, text = "Leave", cursor = "hand2", command = self._on_buttonclick_leave)
        self.info_lb.grid(row = 1, column = 1)
        self.seatinfo.grid(row = 2, column = 1)
        self.lenth_lb.grid(row = 3, column = 1)
        self.total_time.grid(row = 4, column = 1)
        self.empty_lb.grid(row = 5, column = 1)
        self.time_lb.grid(row = 6, column = 1)
        self.leave_btn.grid(row = 7, column = 1)
        self.time_lb.after(1000, self.trickit)
        self.count_time()

    def trickit(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        self.time_lb.config(text = "current time: " + current_time)
        self.frash()
        self.time_lb.after(1000, self.trickit)

    def count_time(self):
        sec = 0
        while True:
            sec += 1
            m, s = divmod(sec, 60)
            h, m = divmod(m, 60)
            self.total_time.config(text = "%d:%02d:%02d" % (h, m, s))
            time.sleep(1)
            self.frash()

    def _on_buttonclick_leave(self):
        #print(self.info)
        pos, floor, room = self.info
        check = messagebox.askyesno("Check", "Do you want to leave")
        if check:
            # #UPDATE INTO DATABASE
            Rid = "'" + floor[-1] + room + "'"
            seat_num = (int(pos[0])-1)*5 + (int(pos[2])-1) + 1
            STid = "'0"
            if seat_num < 10:
                STid += "0" + str(seat_num) + "'"
            else:
                STid += str(seat_num) + "'"
            update_Seats_sql = "update Seats set STstatus = 0 where Rid = " + Rid + " and " + "STid = " + STid
            from dboperate.db import Db
            import time
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            RCDid = current_time[0:4] + current_time[5:7] + current_time[8:10]
            current_time = "'" + current_time + "'"
            num = 0
            db = Db()
            while True:
                tempid = "'" + RCDid + str("%02d" % num) + "'"
                if not db.query("select * from Records where RCDid = " + tempid):
                    break
                else:
                    num += 1
            db.destroy()
            RCDid = tempid
            insert_Records_sql = "insert into Records values (" + RCDid + ", " + str(self.stu[0][0]) + ", " + Rid + ", " + STid + ", " + current_time + ", " + "'student', " + "'leave')"
            try:
                db = Db()
                db.operate(insert_Records_sql)
                db.operate(update_Seats_sql)
            except Exception as e:
                messagebox.showerror("ERROR", e)
            db.destroy()
            self.close()
            FormMainStudent(Tk(), self.stu)