import sqlite3
import requests


class User:

    def __init__(self, user_id, name, username, email, password,
                 user_position):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.user_position = user_position

    @staticmethod
    def user_table_creation(user_position):
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (user_position,))
        if c.fetchone() is None:
            if user_position == 'patient':
                c.execute('''
                            CREATE TABLE IF NOT EXISTS patients (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(255),
                                username VARCHAR(255) UNIQUE,
                                email VARCHAR(255) UNIQUE,
                                password VARCHAR(255)
                            )
                        ''')
            elif user_position == 'doctor':
                c.execute('''
                            CREATE TABLE IF NOT EXISTS doctors (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(255),
                                username VARCHAR(255) UNIQUE,
                                email VARCHAR(255) UNIQUE,
                                password VARCHAR(255)
                            )
                        ''')
            elif user_position == 'secretary':
                c.execute('''
                            CREATE TABLE IF NOT EXISTS secretaries (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(255),
                                username VARCHAR(255) UNIQUE,
                                email VARCHAR(255) UNIQUE,
                                password VARCHAR(255)
                            )
                        ''')
            conn.commit()
            conn.close()


    @classmethod
    def sign_up(cls, name, username, email, password, user_position):
        cls.user_table_creation(user_position)
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        if user_position == 'patient':
            c.execute(
                "INSERT INTO patients (name, username, email, password) VALUES (?,?, ?, ?)",
                (name, username, email, password))
        elif user_position == 'doctor':
            c.execute(
                "INSERT INTO doctors (name, username, email, password) VALUES (?, ?, ?, ?)",
                (name, username, email, password))
        elif user_position == 'secretary':
            c.execute(
                "INSERT INTO secretaries (name, username, email, password) VALUES (?, ?, ?, ?)",
                (name, username, email, password))
        user_id = c.lastrowid
        conn.commit()
        conn.close()
        return cls(user_id, name, username, email, password, user_position)

    @staticmethod
    def sign_in(username, user_position):
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        if user_position == 'patient':
            c.execute("SELECT * FROM patients WHERE username = ?", (username,))
        elif user_position == 'doctor':
            c.execute("SELECT * FROM doctors WHERE username = ?", (username,))
        elif user_position == 'secretary':
            c.execute("SELECT * FROM secretaries WHERE username = ?",
                      (username,))
        user_info = c.fetchone()
        conn.close()
        return user_info
    def update_profile(self, alter, user_position, username, new_value):
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        if user_position == 'patient':
            if alter == 'new_email':
                c.execute("UPDATE patients SET email = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_password':
                c.execute("UPDATE patients SET password = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE patients SET name = ? WHERE username = ?", (new_value, username))
        elif user_position == 'doctor':
            if alter == 'new_email':
                c.execute("UPDATE doctors SET email = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_password':
                c.execute("UPDATE doctors SET password = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE doctors SET name = ? WHERE username = ?", (new_value, username))
        elif user_position == 'secretary':
            if alter == 'new_email':
                c.execute("UPDATE secretaries SET email = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_password':
                c.execute("UPDATE secretaries SET password = ? WHERE username = ?", (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE secretaries SET name = ? WHERE username = ?", (new_value, username))
    

    def meetings(self):
        pass


class Clinic:

    def __init__(self, clinic_id, name, address, contact_info, availability, gp=False, heart=False, dental=False, plastic=False, gp_fee=0, heart_fee=0, dental_fee=0, plastic_fee=0):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.contact_info = contact_info
        self.availability = availability
        self.gp = gp
        self.heart = heart
        self.dental = dental
        self.plastic = plastic
        self.gp_fee = gp_fee
        self.heart_fee = heart_fee
        self.dental_fee = dental_fee
        self.plastic_fee = plastic_fee

    @staticmethod
    def clinic_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='clinics';")
        if c.fetchone() is None:
            c.execute('''
                        CREATE TABLE clinics (
                            clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(255),
                            address VARCHAR(511),
                            contact_info INTEGER UNIQUE,
                            beds_available INTEGER,
                            gp BOOLEAN,
                            heart BOOLEAN,
                            dental BOOLEAN,
                            plastic BOOLEAN,
                            gp_fee INTEGER,
                            heart_fee INTEGER,
                            dental_fee INTEGER,
                            plastic_fee INTEGER
                        )
                    ''')
            conn.commit()
            conn.close()

    @classmethod
    def add_clinic(cls, name, address, contact_info, availability, gp, heart, dental, plastic, gp_fee, heart_fee,dental_fee, plastic_fee):
        cls.clinic_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO clinics (name, address, contact_info, beds_available, gp, heart, dental,plastic, gp_fee, heart_fee,dental_fee, plastic_fee) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            (name, address, contact_info, availability, gp, heart, dental, plastic, gp_fee, heart_fee,dental_fee, plastic_fee))
        clinic_id = c.lastrowid
        conn.commit()
        conn.close()
        return cls(clinic_id, name, address, contact_info, availability, gp, heart, dental, plastic, gp_fee, heart_fee,dental_fee, plastic_fee)

    def getting_clinic_availability(self):

        get_data_url = "http://127.0.0.1:5000/slots"
        response = requests.get(get_data_url)

        if response.status_code != 200:
            raise Exception("The request was not successful!")
        else:
            json_data = response.json()

        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        for clinic_id, availability in json_data.items():
            c.execute('UPDATE clinics SET beds_available = ? WHERE clinic_id = ?',
                      (availability, clinic_id))

        conn.commit()
        conn.close()

    def update_clinic_info(self):
        pass

    def set_availability(self):
        pass

    def view_appointments(self):
        pass


class Appointment:
    def __init__(self, status, datetime, user_id, clinic_id, appointment_id):
        self.status = status
        self.datetime = datetime
        self.user_id = user_id
        self.clinic_id = clinic_id
        self.appointment_id = appointment_id

    def register_appointment(self):
        pass

    def cancel_appointment(self):
        pass

    def reschedule_appointment(self):
        pass


class Notification:
    def __init__(self, notification_id, user_id, message, datetime):
        self.notification_id = notification_id
        self.user_id = user_id
        self.message = message
        self.datetime = datetime

    def send_notification(self):
        pass


class Insurance:
    def __init__(self, name, contact_info, coverage):
        self.name = name
        self.contact_info = contact_info
        self.coverage = coverage

    @staticmethod
    def insurance_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='insurances';")
        if c.fetchone() is None:
            c.execute('''
                        CREATE TABLE insurances (
                            insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(255),
                            contact_info INTEGER UNIQUE,
                            coverage INTEGER
                        )
                    ''')
            conn.commit()
            conn.close()

    @classmethod
    def add_insurance(cls, name, contact_info, coverage):
        cls.insurance_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO insurances (name, contact_info,coverage) VALUES (?,?,?)',
            (name, contact_info, coverage))
        conn.commit()
        conn.close()
        return cls(name, contact_info, coverage)


class Payment:
    def __init__(self, user_id, account_number, cvv2, expiration_date, password):
        self.user = user_id
        self.account_number = account_number
        self.cvv2 = cvv2
        self.expiration_date = expiration_date
        self.password = password

    @staticmethod
    def payment_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='payments';")
        if c.fetchone() is None:
            c.execute('''
                        CREATE TABLE payments (
                            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER,
                            account_number INTEGER,
                            cvv2 INTEGER,
                            expiration_date INTEGER,
                            password INTEGER
                        )
                    ''')
            conn.commit()
            conn.close()

    @classmethod
    def add_payment(cls, user_id, account_number, cvv2, expiration_date, password):
        cls.payment_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO payments (user_id, account_number, cvv2, expiration_date, password) VALUES (?,?,?,?,?)',
            (user_id, account_number, cvv2, expiration_date, password))
        conn.commit()
        conn.close()
        return cls(user_id, account_number, cvv2, expiration_date, password)

    def payment(self):
        pass