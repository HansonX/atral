class Database:
    def __init__(self):
        self.patient_list = []
        self.physician_list = []

    def get_patient_list(self):
        return self.patient_list

    def get_physician_list(self):
        return self.physician_list

    def add_to_patient_list(self, pat):
        self.patient_list.append(pat)

    def add_to_physician_list(self, phys):
        self.physician_list.append(phys)
