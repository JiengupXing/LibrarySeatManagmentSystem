import pymssql as msql

class Db:
    def __init__(self):
        self.host = "(local)"
        self.user = "sa"
        self.passwd = "123456"
        self.database = "LSMS"
        self.charset = "utf8"
        self.connect()
        self.cursor = self.conn.cursor()
    
    def connect(self):
        self.conn = msql.connect(host = self.host, 
                                 user = self.user,
                                 database = self.database,
                                 password = self.passwd, 
                                 charset = self.charset)

    def operate(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        
        except Exception as ex:
            self.conn.rollback()
            raise ex

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        
        except Exception as ex:
            self.conn.rollback()
            raise ex

    def destroy(self):
        self.conn.close()
