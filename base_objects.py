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
            c.execute("SELECT * FROM secretaries WHERE username = ?",
                      (username,))
        user_info = c.fetchone()
        conn.close()
        return user_info

    def update_profile(self):
        pass

    def meetings(self):
        pass


class Clinic:

    def __init__(self, clinic_id, name, address, contact_info, services,
                 availability, fees):
        self.clinic_id = clinic_id
        self.name = name
        self.address = address
        self.contact_info = contact_info
        self.services = services
        self.availability = availability
        self.fees = fees

    @staticmethod
    def clinic_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE clinics (
                        clinic_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(255),
                        address VARCHAR(511),
                        contact_info INTEGER UNIQUE,
                        services VARCHAR(255),
                        beds_available INTEGER,
                        fees VARCHAR(255)
                    )
                ''')
        conn.commit()
        conn.close()

    @classmethod
    def add_clinic(cls, name, address, contact_info, services, availability,
                   fees):
        cls.clinic_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        services_str = ','.join(services)
        fee_str = ','.join(fees)
        c.execute(
            'INSERT INTO clinics (name, address, contact_info, services,beds_available,fees) VALUES (?,?,?,?,?,?)',
            (name, address, contact_info, services_str, availability, fee_str))
        clinic_id = c.lastrowid
        conn.commit()
        conn.close()
        return cls(clinic_id, name, address, contact_info, services,
                   availability, fees)

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
    def __init__(self, name, contact_info, gp_coverage, heart_coverage,
                 dental_coverage, plastic_coverage):
        self.name = name
        self.contact_info = contact_info
        self.gp_coverage = gp_coverage
        self.heart_coverage = heart_coverage
        self.dental_coverage = dental_coverage
        self.plastic_coverage = plastic_coverage

    @staticmethod
    def insurance_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute('''
                    CREATE TABLE insurances (
                        insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(255),
                        contact_info INTEGER UNIQUE,
                        gp_coverage INTEGER,
                        heart_coverage INTEGER,
                        dental_coverage INTEGER,
                        plastic_coverage INTEGER
                    )
                ''')
        conn.commit()
        conn.close()

    @classmethod
    def add_insurance(cls, name, contact_info, gp_coverage, heart_coverage,
                      dental_coverage, plastic_coverage):
        cls.insurance_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO insurances (name, contact_info,gp_coverage,heart_coverage,dental_coverage,plastic_coverage) VALUES (?,?,?,?,?,?)',
            (name, contact_info, gp_coverage, heart_coverage, dental_coverage,
             plastic_coverage))
        conn.commit()
        conn.close()
        return cls(name, contact_info, gp_coverage,
                   heart_coverage, dental_coverage, plastic_coverage)


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