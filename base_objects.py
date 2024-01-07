import sqlite3
import requests
from datetime import datetime
from prettytable import PrettyTable

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
                c.execute("UPDATE patients SET email = ? WHERE username = ?",
                          (new_value, username))
            elif alter == 'new_password':
                c.execute("UPDATE patients SET password = ? WHERE username = ?",
                          (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE patients SET name = ? WHERE username = ?",
                          (new_value, username))
        elif user_position == 'doctor':
            if alter == 'new_email':
                c.execute("UPDATE doctors SET email = ? WHERE username = ?",
                          (new_value, username))
            elif alter == 'new_password':
                c.execute("UPDATE doctors SET password = ? WHERE username = ?",
                          (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE doctors SET name = ? WHERE username = ?",
                          (new_value, username))
        elif user_position == 'secretary':
            if alter == 'new_email':
                c.execute("UPDATE secretaries SET email = ? WHERE username = ?",
                          (new_value, username))
            elif alter == 'new_password':
                c.execute(
                    "UPDATE secretaries SET password = ? WHERE username = ?",
                    (new_value, username))
            elif alter == 'new_name':
                c.execute("UPDATE secretaries SET name = ? WHERE username = ?",
                          (new_value, username))

    @staticmethod
    def meetings(user_id):
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute("""
            SELECT a.reservation_date, a.clinic_id, d.name, p.name, a.payment_amount, a.service
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.user_id
            JOIN patients p ON a.patient_id = p.user_id
            WHERE a.patient_id = ?
        """, (user_id,))
        appointments = c.fetchall()
        conn.close()
        table = PrettyTable()
        table.field_names = ["Reservation Date", "Clinic ID", "Doctor Name",
                             "Patient Name", "Payment Amount", "Service"]
        for appointment in appointments:
            table.add_row(appointment)
        print(table)


class Clinic:

    def __init__(self, clinic_id, name, address, contact_info, availability,
                 gp=False, heart=False, dental=False, plastic=False, gp_fee=0,
                 heart_fee=0, dental_fee=0, plastic_fee=0):
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
    def add_clinic(cls, name, address, contact_info, availability, gp, heart,
                   dental, plastic, gp_fee, heart_fee, dental_fee, plastic_fee):
        cls.clinic_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO clinics (name, address, contact_info, beds_available, gp, heart, dental,plastic, gp_fee, heart_fee,dental_fee, plastic_fee) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            (name, address, contact_info, availability, gp, heart, dental,
             plastic, gp_fee, heart_fee, dental_fee, plastic_fee))
        clinic_id = c.lastrowid
        conn.commit()
        conn.close()
        return cls(clinic_id, name, address, contact_info, availability, gp,
                   heart, dental, plastic, gp_fee, heart_fee, dental_fee,
                   plastic_fee)

    def update_clinic_info(cls, clinic_id, name=None, address=None, contact_info=None, availability=None, gp=None, heart=None, dental=None, plastic=None, gp_fee=None, heart_fee=None, dental_fee=None, plastic_fee=None):
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        if name is not None:
            c.execute('UPDATE clinics SET name = ? WHERE clinic_id = ?', (name, clinic_id))
        if address is not None:
            c.execute('UPDATE clinics SET address = ? WHERE clinic_id = ?', (address, clinic_id))
        if contact_info is not None:
            c.execute('UPDATE clinics SET contact_info = ? WHERE clinic_id = ?', (contact_info, clinic_id))
        if availability is not None:
            c.execute('UPDATE clinics SET beds_available = ? WHERE clinic_id = ?', (availability, clinic_id))
   

        conn.commit()
        conn.close()

    @staticmethod
    def view_appointments(clinic_id):
        conn = sqlite3.connect('ap_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM appointments WHERE clinic_id = ?',
                       (clinic_id,))
        rows = cursor.fetchall()
        conn.close()
        table = PrettyTable()
        table.field_names = ["Appointment ID", "Status", "Reservation Date",
                             "Payment Amount", "Patient ID", "Clinic ID",
                             "Doctor ID", "Insurance ID", "Payment ID", "Service"]
        for row in rows:
            table.add_row(row)
        print(table)



class Appointment:
    def __init__(self, appointment_id, status, reservation_date, payment_amount,
                 patient_id, clinic_id, doctor_id, insurance_id, payment_id, service):
        self.status = status
        self.appointment_id = appointment_id
        self.reservation_date = reservation_date
        self.payment_amount = payment_amount
        self.patient_id = patient_id
        self.clinic_id = clinic_id
        self.doctor_id = doctor_id
        self.insurance_id = insurance_id
        self.payment_id = payment_id
        self.service = service

    @staticmethod
    def appointment_table_creation():
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='appointments';")
        if c.fetchone() is None:
            c.execute('''
                        CREATE TABLE appointments (
                            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            status VARCHAR(255),
                            reservation_date INTEGER,
                            payment_amount INTEGER,
                            patient_id INTEGER,
                            clinic_id INTEGER,
                            doctor_id INTEGER,
                            insurance_id INTEGER,
                            payment_id INTEGER,
                            service VARCHAR(255),
                            FOREIGN KEY(patient_id) REFERENCES patients(user_id),
                            FOREIGN KEY(clinic_id) REFERENCES clinics(clinic_id),
                            FOREIGN KEY(doctor_id) REFERENCES doctors(user_id),
                            FOREIGN KEY(insurance_id) REFERENCES insurances(insurance_id),
                            FOREIGN KEY(payment_id) REFERENCES payments(payment_id)
                        )
                    ''')
            conn.commit()
            conn.close()

    @classmethod
    def add_appointment(cls, status, reservation_date, payment_amount,
                        patient_id, clinic_id, doctor_id, insurance_id,
                        payment_id, service):
        cls.appointment_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO appointments (status, reservation_date,payment_amount,patient_id,clinic_id,doctor_id,insurance_id,payment_id, service) VALUES (?,?,?,?,?,?,?,?,?)',
            (status, reservation_date, payment_amount, patient_id, clinic_id,
             doctor_id, insurance_id, payment_id, service))
        appointment_id = c.lastrowid
        conn.commit()
        conn.close()
        return cls(appointment_id, status, reservation_date, payment_amount,
                   patient_id, clinic_id, doctor_id, insurance_id, payment_id, service)

    @staticmethod
    def register_appointment(clinic_id, reserved_slots, database):
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': clinic_id, 'reserved': reserved_slots}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                remaining_slots = result.get('remaining_slots')
                print(
                    f"Reservation successful. Remaining slots for clinic {clinic_id}: {remaining_slots}")

                # Update the local database dictionary
                if str(clinic_id) in database:
                    database[str(clinic_id)] = remaining_slots
                    print(
                        f"Updated local availability for clinic {clinic_id}: {database[str(clinic_id)]}")
                else:
                    print(f"Invalid clinic ID: {clinic_id}")
            else:
                print("Reservation failed. Invalid request.")
        else:
            print(f"Error: {response.status_code}")

    @staticmethod
    def cancel_appointment(clinic_id, reserved=1):
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': clinic_id, 'reserved': reserved}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            json_data = response.json()
            remaining_slots = json_data['remaining_slots']
            print(f"Clinic {clinic_id} has {remaining_slots}")

        else:
            print(f"Error: {response.status_code}")

    def reschedule_appointment(self, clinic_id, reserved_slots, database):
        # First, cancel the appointment
        self.cancel_appointment(clinic_id, reserved_slots)

        # Then, register the appointment again
        self.register_appointment(clinic_id, reserved_slots, database)

class Notification:
    def __init__(self, user_id, message, date_time):
        self.user_id = user_id
        self.message = message
        self.date_time = date_time

    @classmethod
    def send_notification(cls, user_id):
        message = f"Dear user {user_id}, your appointment is reserved."
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(message)
        return cls(user_id, message, date)


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
    def __init__(self, user_id, account_number, cvv2, expiration_date,
                 password):
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
    def add_payment(cls, user_id, account_number, cvv2, expiration_date,
                    password):
        cls.payment_table_creation()
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO payments (user_id, account_number, cvv2, expiration_date, password) VALUES (?,?,?,?,?)',
            (user_id, account_number, cvv2, expiration_date, password))
        conn.commit()
        conn.close()
        return cls(user_id, account_number, cvv2, expiration_date, password)


