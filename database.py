from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://wiremarrow:admin@cluster0.32wtvyh.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["users"]
        self.patient_list = self.db["patients"]
        self.physician_list = self.db["physicians"]

    def update_db(self):
        self.client = MongoClient("mongodb+srv://wiremarrow:admin@cluster0.32wtvyh.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client["users"]
        self.patient_list = self.db["patients"]
        self.physician_list = self.db["physicians"]

    def get_patient_list(self):
        self.update_db()
        # self.patient_list.find()[0]
        return self.patient_list.find()

    def get_physician_list(self):
        self.update_db()
        # self.physician_list.find()[0]
        return self.physician_list.find()

    def add_to_patient_list(self, f_name=None, l_name=None, username=None, password=None, email=None, age=None, height=None, weight=None, gender=None, sys_bp=None, dia_bp=None, chol=None, glucose=None, is_smoker=None, is_drinker=None, is_active=None):
        self.update_db()
        self.patient_list.insert_one({"f_name": f_name, "l_name": l_name, "username": username, "password": password, "email": email, "age": age, "height": height, "weight": weight, "gender": gender, "sys_bp": sys_bp, "dia_bp": dia_bp, "chol": chol, "glucose": glucose, "is_smoker": is_smoker, "is_drinker": is_drinker, "is_active": is_active})

    def add_to_physician_list(self, f_name=None, l_name=None, username=None, password=None, email=None, age=None, height=None, weight=None, gender=None, sys_bp=None, dia_bp=None, chol=None, glucose=None, is_smoker=None, is_drinker=None, is_active=None):
        self.update_db()
        self.physician_list.insert_one({"f_name": f_name, "l_name": l_name, "username": username, "password": password, "email": email, "age": age, "height": height, "weight": weight, "gender": gender, "sys_bp": sys_bp, "dia_bp": dia_bp, "chol": chol, "glucose": glucose, "is_smoker": is_smoker, "is_drinker": is_drinker, "is_active": is_active})

    def update_patient_record(self, un, n_q):
        self.update_db()
        query = self.patient_list.find_one({'username': f'{un}'})
        new_querry = {'$set': n_q}
        self.patient_list.update_one(query, new_querry)

    def update_physician_record(self, un, n_q):
        self.update_db()
        query = self.physician_list.find_one({'username': f'{un}'})
        new_query = {'$set': n_q}
        self.physician_list.update_one(query, new_query)
