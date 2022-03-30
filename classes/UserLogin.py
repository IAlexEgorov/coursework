class UserLogin:
    def fromDB(self, user_id, user_password, db):
        self.__user = db.getUser(user_id, user_password)
        return self
 
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return str(self.__user['id'])