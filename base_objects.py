import sqlite3


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
            c.execute("SELECT * FROM secretaries WHERE username = ?", (username,))
        user_info = c.fetchone()
        conn.close()
        return user_info

    def update_profile(self):
        pass

    def meetings(self):
        pass


class Clinic:

    def __init__(self, clinic_id, name, address, contact_info, services,
                 availability, heart_fee, dental_fee, short_stay_fee):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.contact_info = contact_info
        self.services = services
        self.availability = availability
        self.heart_fee = heart_fee
        self.dental_fee = dental_fee
        self.short_stay_fee = short_stay_fee

    def add_clinic(self):
        pass

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
    def __init__(self, name, contact_info, heart_fee, dental_fee, short_stay_fee):
        self.name = name
        self.contact_info = contact_info
        self.heart_fee = heart_fee
        self.dental_fee = dental_fee
        self.short_stay_fee = short_stay_fee

    def coverage(self):
        coverage_amounts = {'heart': self.heart_fee, 'dental': self.dental_fee,
                            'short_stay': self.short_stay_fee}


class Payment:
    def __init__(self, user_id, cvv2, expiration_date, password, captcha):
        self.user = user_id
        self.cvv2 = cvv2
        self.expiration_date = expiration_date
        self.password = password
        self.captcha = captcha

    def payment(self):
        pass