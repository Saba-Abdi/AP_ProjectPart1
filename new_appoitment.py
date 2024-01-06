from datetime import datetime
import sqlite3
import time

import requests
from prettytable import PrettyTable
from app import database
from base_objects import Payment, Notification, Appointment


def show_doctors():
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, name FROM doctors')
    rows = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["User ID", "Name"]
    for row in rows:
        table.add_row(row)
    print(table)


def getting_clinic_availability():
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


def show_clinics():
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT clinic_id, name, address, contact_info, beds_available, gp, heart, dental, plastic, gp_fee, heart_fee, dental_fee, plastic_fee FROM clinics')
    rows = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["Clinic ID", "Name", "Address", "Contact Info",
                         "Beds Available", "GP", "Heart", "Dental", "Plastic",
                         "GP Fee", "Heart Fee", "Dental Fee", "Plastic Fee"]

    for row in rows:
        table.add_row(row)

    print(table)


def show_insurances():
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT insurance_id, name, contact_info, coverage FROM insurances')
    rows = cursor.fetchall()
    conn.close()

    table = PrettyTable()
    table.field_names = ["Insurance ID", "Name", "Contact Info", "Coverage"]
    for row in rows:
        table.add_row(row)
    print(table)


def payment_amount(position, username, doctor, clinic, service, insurance=None):
    conn = sqlite3.connect('ap_database.db')
    c = conn.cursor()

    if insurance != '':
        c.execute('SELECT coverage FROM insurances WHERE insurance_id = ?',
                  (insurance,))
        insurance_coverage_percentage = c.fetchone()

        if insurance_coverage_percentage:
            insurance_coverage = insurance_coverage_percentage[0] / 100
            service_fee_column = f"{service}_fee"
            c.execute(
                f'SELECT {service_fee_column} FROM clinics WHERE clinic_id = ?',
                (clinic,))
            service_fee = c.fetchone()

            if service_fee:
                appointment_price = service_fee[0] * (
                            1 - insurance_coverage)
                return check_price(position, username, doctor, clinic, service, appointment_price, insurance)
            else:
                print("Service fee not found for the clinic")

        else:
            print(
                "Insurance coverage percentage not found for the insurance")

    else:
        c.execute('SELECT service_fee FROM clinics WHERE clinic_id = ?',
                  (clinic,))
        service_fee = c.fetchone()

        if service_fee:
            appointment_price = service_fee[0]
            return check_price(position, username, doctor, clinic, service, appointment_price, insurance)
        else:
            print("Service fee not found for the clinic")

    conn.close()


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
            Appointment.add_appointment("reserved", date, price, user_id, clinic, doctor, insurance, payment_id, service)

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
