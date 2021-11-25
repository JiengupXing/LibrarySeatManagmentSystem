from .db import Db
import pandas as pd

def importcsvfile(db, table):
    file = "data/" + table + ".csv"
    data = pd.read_csv(file, header = None)
    for index, row in data.iterrows():
        sql = "insert into " + table + " values("
        ls = row.tolist()
        for item in ls:
            sql += str(item) + ""
            if item != ls[-1]:
                sql += ", "
        sql += ")"
        db.operate(sql)
    print("data in " + table + ".csv" + " has imported successfully!")

def ImportData():
    db = Db()
    importcsvfile(db, "Institutes")
    importcsvfile(db, "Students")
    importcsvfile(db, "Librarians")
    importcsvfile(db, "Rooms")
    importcsvfile(db, "Seats")
    importcsvfile(db, "Records")
    db.destroy()