from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import ttk
from tkinter import messagebox
from .form import Form
from .formmain import FormMainStudent
import sys
import time

class FormManageImport(Form):
    def __init__(self, master, usr_info):
        Frame.__init__(self, master)
        self._initialize(master, usr_info)
        self._initialize_view(master)

    def _initialize(self, master, usr_info):
        self.info = usr_info
        self.short_to_id = {}
        self.instituteshort = []
        #SELECT INSTITUTESHORT
        from dboperate.db import Db
        try:
            db = Db()
            institu_short = db.query("select Iid, Ishort from Institutes")
            for item in institu_short:
                self.short_to_id[item[1]] = str(item[0])
                self.instituteshort.append(item[1])
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
        #SELECT IID
        self.Iid = StringVar()

    def _initialize_view(self, master):
        self.master.title("Import Page")
        self.uid_lb = Label(master, text = "User_ID: ")
        self.uid_ety = Entry(master)
        self.passwd_lb = Label(master, text = "Password: ")
        self.passwd_ety = Entry(master)
        self.name_lb = Label(master, text = "name: ")
        self.name_ety = Entry(master)
        self.sex_lb = Label(master, text = "sex: ")
        self.sex_cbb = ttk.Combobox(master, state = "readonly", values = ("m", "f"))
        self.age_lb = Label(master, text = "age: ")
        self.age_ety = Entry(master)
        self.Iid_lb = Label(master, text = "Institute ID: ")
        self.Iid_ety = Entry(master, textvariable = self.Iid, state = "readonly")
        self.class_lb = Label(master, text = "class: ")
        self.class_ety = Entry(master)
        self.major_lb = Label(master, text =  "major")
        self.major_ety = Entry(master)
        self.instiname_lb = Label(master, text = "Institute name: ")
        self.instiname_cbb = ttk.Combobox(master, state = "readonly", value = ["COI", "COPS", "COS", "COF"])
        self.btn_confirm = Button(master, text = "confirm", command = self._on_buttonclick_confirm)
        self.btn_back = Button(master, text = "back", command = self._on_buttonclick_back)

        self.uid_lb.grid(row = 1, column = 1)
        self.uid_ety.grid(row = 1, column = 2)
        self.passwd_lb.grid(row = 2, column = 1)
        self.passwd_ety.grid(row = 2, column = 2)
        self.name_lb.grid(row = 3, column = 1)
        self.name_ety.grid(row = 3, column = 2)
        self.sex_lb.grid(row = 4, column = 1)
        self.sex_cbb.grid(row = 4, column = 2)
        self.age_lb.grid(row = 5, column = 1)
        self.age_ety.grid(row = 5, column = 2)
        self.Iid_lb.grid(row = 6, column = 1)
        self.Iid_ety.grid(row = 6, column = 2)
        self.class_lb.grid(row = 7, column = 1)
        self.class_ety.grid(row = 7, column = 2)
        self.major_lb.grid(row = 8, column = 1)
        self.major_ety.grid(row = 8, column = 2)
        self.instiname_lb.grid(row = 9, column = 1)
        self.instiname_cbb.grid(row = 9, column = 2)
        self.btn_confirm.grid(row = 10, column = 1)
        self.btn_back.grid(row =10, column = 2)
        self.instiname_cbb.bind("<<ComboboxSelected>>", self._on_combobox_selected)


    def _on_combobox_selected(self, event = None):
        short = self.instiname_cbb.get()
        self.Iid.set(self.short_to_id[short])


    def _on_buttonclick_confirm(self):
        check = messagebox.askyesno("CHECK", "Are you sure to creat a new student user?")
        if check:
            uid = self.uid_ety.get()
            passwd = self.passwd_ety.get()
            name = self.name_ety.get()
            sex = self.sex_cbb.get()
            age = self.age_ety.get()
            iid = self.Iid_ety.get()
            sclass = self.class_ety.get()
            major = self.major_ety.get()
            short = self.instiname_cbb.get()
            insert_sql = "insert into Students values(" + uid + ", '" + passwd + "', " + "'" + name + "', " + "'" + sex + "', " + age + ", " + iid + ", '" + sclass + "', '" + major + "', " + "'" + short + "')"
            #INSERT INTO STUDENTS
            from dboperate.db import Db
            try:
                db = Db()
                db.operate(insert_sql)
            except Exception as e:
                messagebox.showerror("ERROR", e)
            db.destroy()

    def _on_buttonclick_back(self):
        from .formmain import FormMainAdministor
        self.close()
        FormMainAdministor(Tk(), self.info)

    
class FormManageQuery(Form):
    def __init__(self, master, usr_info):
        Frame.__init__(self, master)
        self._initialize(master, usr_info)
        self._initialize_view(master)

    def _initialize(self, master, usr_info):
        self.info = usr_info
        self.records = ["RCDid, Uid, Rid, STid, Rtime, Operate_type, Operation"]
        self.master
        from dboperate.db import Db
        try:
            db = Db()
            query_sql = "select * from Records order by Rtime desc"
            records = db.query(query_sql)
            for item in records:
                item = list(item)
                item[1] = str(item[1])
                item[4] = item[4].strftime("%Y-%m-%d %H:%M:%S")
                record = ""
                for j in item:
                    record = record + j + ", "
                self.records.append(record)
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
    def _initialize_view(self, master):
        self.master.title("Records Page")
        self.master.geometry("800x720")
        self.sb = Scrollbar(master)
        self.sb.pack(side = RIGHT, fill = Y, expand = True)
        self.lb = Listbox(master, yscrollcommand = self.sb.set)
        for item in self.records:
            self.lb.insert(END, item)
        self.lb.pack(side =LEFT, fill = BOTH, expand = True)
        self.sb.config(command = self.lb.yview)
        self.btn = Button(text = "back", command = self._on_buttonclick_back)
        self.btn.pack(side = BOTTOM)
    def _on_buttonclick_back(self):
        from .formmain import FormMainAdministor
        self.close()
        FormMainAdministor(Tk(), self.info)


class FormManageLock(Form):
    def __init__(self, master, usr_info):
        Frame.__init__(self, master)
        self._initialize(master, usr_info)
        self._initialize_view(master)

    def _initialize(self, master, usr_info):
        self.info = usr_info
        self.img_seat_takable = PhotoImage(file = "img/seat_takable.png")
        self.img_seat_taken = PhotoImage(file = "img/seat_taken.png")

    def _initialize_view(self, master):
        self.master.title("Lock Page")
        self.fra_left = Frame(master)
        self.btn_back = Button(self.fra_left, text = "back", command = self._on_buttonclick_back)
        #.encode('latin-1').decode('gbk')
        self.fra_right = Frame(master)
        self.floor_lab = Label(self.fra_right, text = "Floors", font = font.Font(size = 15, weight = "bold"))
        floors = ("floor1", "floor2")
        self.cmb_floor = ttk.Combobox(self.fra_right, state = "readonly", values = floors)
        self.room_lab = Label(self.fra_right, text = "Rooms", font = font.Font(size = 15, weight = "bold"))
        rooms = ("01", "02", "03")
        self.cmb_room = ttk.Combobox(self.fra_right, state = "readonly", values = rooms)
        self.btn_back.grid(row = 1, column = 1)
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
                    self.seats_btn_list[i][j]["state"] = "normal"
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
    
    def _on_buttonclick_back(self):
        from .formmain import FormMainAdministor
        self.close()
        FormMainAdministor(Tk(), self.info)


    def _on_button_clicked(self, btn):
        floor = self.cmb_floor.get()
        room = self.cmb_room.get()
        pos = btn["text"]
        if floor == "" or room == "":
            messagebox.showerror("ERROR!", "please select floor and room")
        else:
            check = messagebox.askyesno(title = "Make Sure", message = "Are you sure to lock this\n" + pos  + " seat\nin ROOM " + floor[-1] + room + " of " + floor.upper() + "?")
            if check == True:
                self.lock_a_seat(pos = pos, floor = floor, room = room)


    def lock_a_seat(self, pos, floor, room):
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
        insert_Records_sql = "insert into Records values (" + RCDid + ", " + str(self.info[0][0]) + ", " + Rid + ", " + STid + ", " + current_time + ", " + "'administor', " + "'lock')"
        try:
            db = Db()
            db.operate(insert_Records_sql)
            db.operate(update_Seats_sql)
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()

        


class FormManageStatics(Form):
    def __init__(self, master, usr_info):
        Frame.__init__(self, master)
        self._initialize(master, usr_info)
        self._initialize_view(master)

    def _initialize(self, master, usr_info):
        self.info = usr_info
        self.short_to_id = {}
        self.instituteshort = []
        #SELECT INSTITUTESHORT
        from dboperate.db import Db
        try:
            db = Db()
            institu_short = db.query("select Iid, Ishort from Institutes")
            for item in institu_short:
                self.short_to_id[item[1]] = str(item[0])
                self.instituteshort.append(item[1])
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
        #SELECT IID
        self.Iid = StringVar()

    def _initialize_view(self, master):
        self.id_to_short = {}
        #SELECT INSTITUTESHORT
        from dboperate.db import Db
        try:
            db = Db()
            institu_short = db.query("select Iid, Ishort from Institutes")
            for item in institu_short:
                self.id_to_short[str(item[0])] = item[1]
        except Exception as e:
            messagebox.showerror("ERROR", e)
        db.destroy()
        import pandas as pd
        import sys
        from dboperate.db import Db
        try:
            db = Db()
            static_sql = "select Iid,count(Iid) from Students where Uid in (select Records.Uid from Records, Students where Records.Uid = Students.Uid) group by Iid"
            statics = db.query(static_sql)
        except Exception as e:
            messagebox.showerror("ERROR", e) 
        db.destroy()
        static_dic = {}
        for item in statics:
            Iid = str(item[0])
            static_dic[self.id_to_short[Iid]] = item[1]
        static_cnt = pd.Series(static_dic)
        fig = static_cnt.plot(kind = "bar").get_figure()
        fig.savefig("cuts/temp.png")
    # fig = cnt.plot(kind = "bar").get_figure()
        # fig.savefig("fig.png")
        # label_dis = df.label.value_counts()
        # ax = label_dis.plot(title='label distribution'， kind='bar'， figsize=(18， 12))
        # fig = ax.get_figure()
        # fig.savefig('label_distribution.png')

    def _initialize_view(self, master):
        self.master.title("Statics")
        self.statics_img = PhotoImage(file = "cuts/temp.png")
        self.statics_lb = Label(master, image = self.statics_img)
        self.button_back = Button(master, text = "back", command = self._on_buttonclick_back)
        self.statics_lb.grid(row = 1, column = 1)
        self.button_back.grid(row = 2, column = 1)
    
    def _on_buttonclick_back(self):
        from .formmain import FormMainAdministor
        self.close()
        FormMainAdministor(Tk(), self.info)