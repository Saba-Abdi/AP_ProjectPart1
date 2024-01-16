# Importing necessary libraries
import sqlite3
import requests
from datetime import datetime
from prettytable import PrettyTable


# Defining the User class
class User:
    # Initializer / Instance attributes
    def __init__(self, user_id, name, username, email, password,
                 user_position):
        self.user_id = user_id
        self.username = username
        self.name = name
        self.email = email
        self.password = password
        self.user_position = user_position

    # Method to create a new table for each user position if it doesn't exist
    @staticmethod
    def user_table_creation(user_position):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Check if a table for the user position already exists
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
            (user_position,))

        # If the table doesn't exist, create a new one
        if c.fetchone() is None:
            if user_position == 'patient':
                # Create a new table for patients
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
                # Create a new table for doctors
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
                # Create a new table for secretaries
                c.execute('''
                            CREATE TABLE IF NOT EXISTS secretaries (
                                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name VARCHAR(255),
                                username VARCHAR(255) UNIQUE,
                                email VARCHAR(255) UNIQUE,
                                password VARCHAR(255)
                            )
                        ''')
            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    # Class method to sign up a new user
    @classmethod
    def sign_up(cls, name, username, email, password, user_position):
        # Create a new table for the user position if it doesn't exist
        cls.user_table_creation(user_position)

        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Insert the new user's details into the appropriate table
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

        # Get the ID of the last inserted row
        user_id = c.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return a new instance of the class with the new user's details
        return cls(user_id, name, username, email, password, user_position)

    # Static method to sign in a user
    @staticmethod
    def sign_in(username, user_position):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Select the user's details from the appropriate table
        if user_position == 'patient':
            c.execute("SELECT * FROM patients WHERE username = ?", (username,))
        elif user_position == 'doctor':
            c.execute("SELECT * FROM doctors WHERE username = ?", (username,))
        elif user_position == 'secretary':
            c.execute("SELECT * FROM secretaries WHERE username = ?",
                      (username,))

        # Fetch the user's details
        user_info = c.fetchone()

        # Close the connection
        conn.close()

        # Return the user's details
        return user_info

    # Method to update a user's profile
    def update_profile(self, alter, user_position, username, new_value):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Update the user's details in the appropriate table
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

        # Static method to retrieve a user's meetings
    @staticmethod
    def meetings(user_id):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Execute a SQL query to retrieve the user's appointments
        c.execute("""
            SELECT a.reservation_date, a.clinic_id, d.name, p.name, a.payment_amount, a.service
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.user_id
            JOIN patients p ON a.patient_id = p.user_id
            WHERE a.patient_id = ?
        """, (user_id,))

        # Fetch all the appointments
        appointments = c.fetchall()

        # Close the connection
        conn.close()

        # Create a table to display the appointments
        table = PrettyTable()
        table.field_names = ["Reservation Date", "Clinic ID", "Doctor Name",
                            "Patient Name", "Payment Amount", "Service"]

        # Add each appointment to the table
        for appointment in appointments:
            table.add_row(appointment)

        # Print the table
        print(table)

    # Defining the Clinic class
class Clinic:

        # Initializer / Instance attributes
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

    # Static method to create a new table for clinics if it doesn't exist
    @staticmethod
    def clinic_table_creation():
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Check if a table for clinics already exists
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='clinics';")

        # If the table doesn't exist, create a new one
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
            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    # Class method to add a new clinic
    @classmethod
    def add_clinic(cls, name, address, contact_info, availability, gp, heart,
                   dental, plastic, gp_fee, heart_fee, dental_fee, plastic_fee):
        # Create a new table for clinics if it doesn't exist
        cls.clinic_table_creation()

        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Insert the new clinic's details into the clinics table
        c.execute(
            'INSERT INTO clinics (name, address, contact_info, beds_available, gp, heart, dental,plastic, gp_fee, heart_fee,dental_fee, plastic_fee) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
            (name, address, contact_info, availability, gp, heart, dental,
             plastic, gp_fee, heart_fee, dental_fee, plastic_fee))

        # Get the ID of the last inserted row
        clinic_id = c.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return a new instance of the class with the new clinic's details
        return cls(clinic_id, name, address, contact_info, availability, gp,
                   heart, dental, plastic, gp_fee, heart_fee, dental_fee,
                   plastic_fee)

    # Method to update a clinic's information
    def update_clinic_info(cls, clinic_id, name=None, address=None,
                           contact_info=None, availability=None, gp=None,
                           heart=None, dental=None, plastic=None, gp_fee=None,
                           heart_fee=None, dental_fee=None, plastic_fee=None):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Update the clinic's details in the clinics table
        if name is not None:
            c.execute('UPDATE clinics SET name = ? WHERE clinic_id = ?',
                      (name, clinic_id))
        if address is not None:
            c.execute('UPDATE clinics SET address = ? WHERE clinic_id = ?',
                      (address, clinic_id))
        if contact_info is not None:
            c.execute('UPDATE clinics SET contact_info = ? WHERE clinic_id = ?',
                      (contact_info, clinic_id))
        if availability is not None:
            c.execute(
                'UPDATE clinics SET beds_available = ? WHERE clinic_id = ?',
                (availability, clinic_id))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

    # Static method to view a clinic's appointments
    @staticmethod
    def view_appointments(clinic_id):
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        cursor = conn.cursor()

        # Execute a SQL query to retrieve the clinic's appointments
        cursor.execute('SELECT * FROM appointments WHERE clinic_id = ?',
                       (clinic_id,))

        # Fetch all the appointments
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        # Create a table to display the appointments
        table = PrettyTable()
        table.field_names = ["Appointment ID", "Status", "Reservation Date",
                             "Payment Amount", "Patient ID", "Clinic ID",
                             "Doctor ID", "Insurance ID", "Payment ID"]

        # Add each appointment to the table
        for row in rows:
            table.add_row(row)

        # Print the table
        print(table)


# Defining the Appointment class
class Appointment:
    # Initializer / Instance attributes
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

    # Static method to create a new table for appointments if it doesn't exist
    @staticmethod
    def appointment_table_creation():
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Check if a table for appointments already exists
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='appointments';")

        # If the table doesn't exist, create a new one
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
            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    # Class method to add a new appointment
    @classmethod
    def add_appointment(cls, status, reservation_date, payment_amount,
                        patient_id, clinic_id, doctor_id, insurance_id,
                        payment_id, service):
        # Create a new table for appointments if it doesn't exist
        cls.appointment_table_creation()

        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Insert the new appointment's details into the appointments table
        c.execute(
            'INSERT INTO appointments (status, reservation_date,payment_amount,patient_id,clinic_id,doctor_id,insurance_id,payment_id, service) VALUES (?,?,?,?,?,?,?,?,?)',
            (status, reservation_date, payment_amount, patient_id, clinic_id,
             doctor_id, insurance_id, payment_id, service))

        # Get the ID of the last inserted row
        appointment_id = c.lastrowid

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return a new instance of the class with the new appointment's details
        return cls(appointment_id, status, reservation_date, payment_amount,
                   patient_id, clinic_id, doctor_id, insurance_id, payment_id,
                   service)

    # Static method to register an appointment
    @staticmethod
    def register_appointment(clinic_id, reserved_slots, database):
        # Define the URL and data for the POST request
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': clinic_id, 'reserved': reserved_slots}
        # Send the POST request
        response = requests.post(url, json=data)
        # Check the status code of the response
        if response.status_code == 200:
            # If the status code is 200, the request was successful
            result = response.json()
            if result.get('success'):
                # If the reservation was successful, print a success message
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

    # Static method to cancel an appointment
    @staticmethod
    def cancel_appointment(clinic_id, reserved=1):
        # Define the URL and data for the POST request
        url = 'http://127.0.0.1:5000/reserve'
        data = {'id': clinic_id, 'reserved': reserved}
        response = requests.post(url, json=data)
        # Check the status code of the response
        if response.status_code == 200:
            json_data = response.json()
            remaining_slots = json_data['remaining_slots']
            print(f"Clinic {clinic_id} has {remaining_slots}")

        else:
            print(f"Error: {response.status_code}")

    # Method to reschedule an appointment
    def reschedule_appointment(self, clinic_id, reserved_slots, database):
        # First, cancel the appointment
        self.cancel_appointment(clinic_id, reserved_slots)

        # Then, register the appointment again
        self.register_appointment(clinic_id, reserved_slots, database)

# Defining the Notification class
class Notification:
    def __init__(self, message, date_time, user_id=None):
        self.user_id = user_id
        self.message = message
        self.date_time = date_time

    # Class method to send a notification
    @classmethod
    def reserve_notification(cls, user_id):
        # Define the message and current date and time
        message = f"Dear user {user_id}, your appointment is reserved."
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(message)
        return cls(user_id, message, date)

    @classmethod
    def increase_notification(cls, clinic_name, number):
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message = f"Dear user, you successfully increased availability of {clinic_name} by the number {number}. "
        print(message)
        return cls(message, date)

    @classmethod
    def cancel_notification(cls, appointment_id):
        current_datetime = datetime.now()
        date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        message = f"The appointment {appointment_id} is cancelled."
        print(message)
        return cls(message, date)

# Defining the Insurance class
class Insurance:
    # Initializer / Instance attributes
    def __init__(self, name, contact_info, coverage):
        self.name = name
        self.contact_info = contact_info
        self.coverage = coverage

    # Static method to create a new table for insurances if it doesn't exist
    @staticmethod
    def insurance_table_creation():
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Check if a table for insurances already exists
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='insurances';")

        # If the table doesn't exist, create a new one
        if c.fetchone() is None:
            c.execute('''
                        CREATE TABLE insurances (
                            insurance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name VARCHAR(255),
                            contact_info INTEGER UNIQUE,
                            coverage INTEGER
                        )
                    ''')
            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    # Class method to add a new insurance
    @classmethod
    def add_insurance(cls, name, contact_info, coverage):
        # Create a new table for insurances if it doesn't exist
        cls.insurance_table_creation()

        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Insert the new insurance's details into the insurances table
        c.execute(
            'INSERT INTO insurances (name, contact_info,coverage) VALUES (?,?,?)',
            (name, contact_info, coverage))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return a new instance of the class with the new insurance's details
        return cls(name, contact_info, coverage)


# Defining the Payment class
class Payment:
    # Initializer / Instance attributes
    def __init__(self, user_id, account_number, cvv2, expiration_date,
                 password):
        self.user = user_id
        self.account_number = account_number
        self.cvv2 = cvv2
        self.expiration_date = expiration_date
        self.password = password

    # Static method to create a new table for payments if it doesn't exist
    @staticmethod
    def payment_table_creation():
        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Check if a table for payments already exists
        c.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='payments';")

        # If the table doesn't exist, create a new one
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
            # Commit the changes and close the connection
            conn.commit()
            conn.close()

    # Class method to add a new payment
    @classmethod
    def add_payment(cls, user_id, account_number, cvv2, expiration_date,
                    password):
        # Create a new table for payments if it doesn't exist
        cls.payment_table_creation()

        # Connect to the SQLite database
        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()

        # Insert the new payment's details into the payments table
        c.execute(
            'INSERT INTO payments (user_id, account_number, cvv2, expiration_date, password) VALUES (?,?,?,?,?)',
            (user_id, account_number, cvv2, expiration_date, password))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Return a new instance of the class with the new payment's details
        return cls(user_id, account_number, cvv2, expiration_date, password)
