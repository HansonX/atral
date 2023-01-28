class Database:
    def __init__(self):
        self.user_list = []
        self.patient_list = []
        self.physician_list = []

    def get_user_list(self):
        return self.user_list

    def get_patient_list(self):
        return self.patient_list

    def get_physician_list(self):
        return self.physician_list

    def add_to_user_list(self, user):
        self.user_list.append(user)

    def add_to_patient_list(self, pat):
        self.patient_list.append(pat)

    def add_to_physician_list(self, phys):
        self.physician_list.append(phys)
