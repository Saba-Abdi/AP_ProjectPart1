# Importing necessary libraries and modules
from datetime import datetime
import sqlite3
import time
import requests
from prettytable import PrettyTable
from app import database
from base_objects import Payment, Notification, Appointment


# Function to display doctors
def show_doctors():
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to retrieve all doctors
    cursor.execute('SELECT user_id, name FROM doctors')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a table to display the doctors
    table = PrettyTable()
    table.field_names = ["User ID", "Name"]

    # Add each doctor to the table
    for row in rows:
        table.add_row(row)

    # Print the table
    print(table)


# Function to get clinic availability
def getting_clinic_availability():
    # URL to get data
    get_data_url = "http://127.0.0.1:5000/slots"

    # Send a GET request to the URL
    response = requests.get(get_data_url)

    # If the request was not successful, raise an exception
    if response.status_code != 200:
        raise Exception("The request was not successful!")
    else:
        # Parse the JSON data from the response
        json_data = response.json()

    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    c = conn.cursor()

    # For each clinic in the data, update its availability in the database
    for clinic_id, availability in json_data.items():
        c.execute('UPDATE clinics SET beds_available = ? WHERE clinic_id = ?',
                  (availability, clinic_id))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Function to display clinics
def show_clinics():
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to retrieve all clinics
    cursor.execute(
        'SELECT clinic_id, name, address, contact_info, beds_available, gp, heart, dental, plastic, gp_fee, heart_fee, dental_fee, plastic_fee FROM clinics')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a table to display the clinics
    table = PrettyTable()
    table.field_names = ["Clinic ID", "Name", "Address", "Contact Info",
                         "Beds Available", "GP", "Heart", "Dental", "Plastic",
                         "GP Fee", "Heart Fee", "Dental Fee", "Plastic Fee"]

    # Add each clinic to the table
    for row in rows:
        table.add_row(row)

    # Print the table
    print(table)


# Function to display insurances
def show_insurances():
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to retrieve all insurances
    cursor.execute(
        'SELECT insurance_id, name, contact_info, coverage FROM insurances')
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a table to display the insurances
    table = PrettyTable()
    table.field_names = ["Insurance ID", "Name", "Contact Info", "Coverage"]

    # Add each insurance to the table
    for row in rows:
        table.add_row(row)

    # Print the table
    print(table)


# Function to calculate the payment amount
def payment_amount(position, username, doctor, clinic, service, insurance=None):
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    c = conn.cursor()

    # If the user has insurance
    if insurance != '':
        # Execute a SQL query to retrieve the coverage of the insurance
        c.execute('SELECT coverage FROM insurances WHERE insurance_id = ?',
                  (insurance,))
        insurance_coverage_percentage = c.fetchone()

        # If the insurance coverage percentage was found
        if insurance_coverage_percentage:
            # Calculate the insurance coverage
            insurance_coverage = insurance_coverage_percentage[0] / 100
            service_fee_column = f"{service}_fee"

            # Execute a SQL query to retrieve the service fee of the clinic
            c.execute(
                f'SELECT {service_fee_column} FROM clinics WHERE clinic_id = ?',
                (clinic,))
            service_fee = c.fetchone()

            # If the service fee was found
            if service_fee:
                # Calculate the appointment price
                appointment_price = service_fee[0] * (
                        1 - insurance_coverage)
                return check_price(position, username, doctor, clinic, service,
                                   appointment_price, insurance)
            else:
                print("Service fee not found for the clinic")

        else:
            print(
                "Insurance coverage percentage not found for the insurance")

    # If the user doesn't have insurance
    else:
        # Execute a SQL query to retrieve the service fee of the clinic
        c.execute('SELECT service_fee FROM clinics WHERE clinic_id = ?',
                  (clinic,))
        service_fee = c.fetchone()

        # If the service fee was found
        if service_fee:
            # The appointment price is the service fee
            appointment_price = service_fee[0]
            return check_price(position, username, doctor, clinic, service,
                               appointment_price, insurance)
        else:
            print("Service fee not found for the clinic")

    # Close the connection
    conn.close()


# Function to choose a service
def choose_service(position, username):
    print("This is the list of all doctors:")
    show_doctors()
    doctor = input("Please choose a doctor (Please enter the doctor id): ")
    print("This is the list of all clinics")
    show_clinics()
    clinic = input("Please choose a clinic (Please enter the clinic id): ")
    service = input("Please choose the service you want: ")
    print(
        "This is the list of insurance companies we work with. Please choose your insurance if you have one")
    show_insurances()
    insurance = input(
        "Please choose your insurance (Please enter the insurance id): ")
    return payment_amount(position, username, doctor, clinic, service,
                          insurance)


# Function to check the price of a service
def check_price(position, username, doctor, clinic, service, price, insurance):
    print(
        f"The price of your service considering your insurance will be {price}")
    answer = input("Do you still want to reserve? yes or no?")
    if answer == "no":
        print("The appointment reservation is declined.")
    elif answer == "yes":
        print("Please enter your payment information")
        account_number = input("Please enter your account number: ")
        cvv2 = input("Please enter your cvv2: ")
        expiration_date = input("Please enter your card expiration date: ")
        password = input("Please enter your password: ")

        conn = sqlite3.connect('ap_database.db')
        c = conn.cursor()
        c.execute('SELECT user_id FROM patients WHERE username = ?',
                  (username,))
        result = c.fetchone()
        conn.close()
        if result:
            user_id = result[0]
            print("Payment is in progress. it may take seconds, please wait.")
            Payment.add_payment(user_id, account_number, cvv2, expiration_date,
                                password)
            time.sleep(5)
            print("Payment was successful")
            print("Your appointment is reserved")
            Notification.send_notification(user_id)
            current_datetime = datetime.now()
            date = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('ap_database.db')
            c = conn.cursor()
            c.execute(
                'SELECT payment_id FROM payments ORDER BY payment_id DESC LIMIT 1')
            result = c.fetchone()
            conn.close()
            payment_id = result[0]
            Appointment.add_appointment("reserved", date, price, user_id,
                                        clinic, doctor, insurance, payment_id,
                                        service)

            conn = sqlite3.connect('ap_database.db')
            c = conn.cursor()

            c.execute('''
                    UPDATE clinics
                    SET beds_available = beds_available - ?
                    WHERE clinic_id = ?
                ''', (1, clinic))

            conn.commit()
            conn.close()
            return Appointment.register_appointment(clinic, 1, database)
