class User:
    def __init__(self, un, pw):
        self.username = un
        self.password = pw
        self.authenticated = True
        self.active = True
        self.anonymous = False

    def get_id(self):
        return self.username

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return self.anonymous

    def set_username(self, un):
        self.username = un

    def set_password(self, pw):
        self.password = pw

    def set_authentication(self, x):
        self.authenticated = x

    def set_activity(self, x):
        self.active = x

    def set_anonymity(self, x):
        self.anonymous = x

class Patient(User):
    def __init__(self, un, pw):
        User.__init__(self, un, pw)

class Physician(User):
    def __init__(self, un, pw):
        User.__init__(self, un, pw)
