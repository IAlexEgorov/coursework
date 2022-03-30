import sqlite3
 
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def checkUser(self, username, password):
        try:
            self.__cur.execute(f"SELECT * FROM Clients WHERE u_login = '{ username }' and u_password = '{ password }' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return True
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))
 
        return False
    
    def getUser(self, username):
        try:
            self.__cur.execute(f"SELECT * FROM Clients WHERE u_login = '{ username }' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return True
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД "+str(e))

        return False
    