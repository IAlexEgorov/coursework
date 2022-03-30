import sqlite3
 
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
 
    def getUserName(self, username):
        sql = 'SELECT * FROM Clients'
        try:
            self.__cur.execute(sql)
            records = self.__cur.fetchone()
            return records[0]
        except:
            print("Ошибка чтения из БД")
        return []

    