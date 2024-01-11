# Importing necessary libraries and modules
from base_objects import *
import sqlite3
from prettytable import PrettyTable

# Connect to the SQLite database
conn = sqlite3.connect('ap_database.db')
c = conn.cursor()


# Function to handle different requests
def manoeuvre(request):
    # If the request is 1, show appointments
    if request == 1:
        doc = input(
            'Would you like to view the appointments for a specific doctor? If so, please enter his/her id. Otherwise, I can display all appointments.(Please enter all)')
        hosp = input(
            'Would you like to view the appointments for a specific hospital? If so, please enter its id. Otherwise, I can display all appointments.(Please enter all)')

        # If the user wants to see all appointments
        if doc == 'all' and hosp == 'all':
            c.execute("SELECT * FROM appointments")
            results = c.fetchall()

            # Create a table to display the appointments
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]

            # Add each appointment to the table
            for row in results:
                table.add_row(row)

            # Print the table
            print(table)

        # If the user wants to see appointments for a specific doctor
        elif doc != 'all' and hosp == 'all':
            doc = int(doc)
            c.execute('SELECT * FROM appointments WHERE doctor_id = ?', (doc,))
            results = c.fetchall()

            # Create a table to display the appointments
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]

            # Add each appointment to the table
            for row in results:
                table.add_row(row)

            # Print the table
            print(table)

        # If the user wants to see appointments for a specific hospital
        elif doc == 'all' and hosp != 'all':
            hosp = int(hosp)
            c.execute('SELECT * FROM appointments WHERE clinic_id = ?', (hosp,))
            results = c.fetchall()

            # Create a table to display the appointments
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]

            # Add each appointment to the table
            for row in results:
                table.add_row(row)

            # Print the table
            print(table)

        # If the user wants to see appointments for a specific doctor and hospital
        else:
            doc = int(doc)
            hosp = int(hosp)
            c.execute(
                'SELECT * FROM appointments WHERE doctor_id = ? AND clinic_id = ?',
                (doc, hosp))
            results = c.fetchall()

            # Create a table to display the appointments
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]

            # Add each appointment to the table
            for row in results:
                table.add_row(row)

            # Print the table
            print(table)

    # If the request is 2, cancel an appointment
    elif request == 2:
        appointment_id = input(
            'Please enter ID of the appointment which you wish to delete')
        clinic_id = input(
            'Please enter ID of the clinic which you wish to delete')
        c.execute(
            'DELETE FROM appointments WHERE appointment_id = ?',
            (appointment_id)
        )

        # Update the availability of the clinic
        c.execute("""
                    UPDATE clinics
                    SET beds_available = beds_available + ?
                    WHERE clinic_id = ?
                """, (1, clinic_id))

        # Commit the changes
        conn.commit()
        print("The appointment is cancelled")

    # If the request is 3, increase the number of available beds in a clinic
    elif request == 3:
        clinic_name = input(
            'Please enter the name of the clinic for which you wish to increase the number of available beds.')
        num = int(input('How many more beds?'))

        # Update the availability of the clinic
        c.execute("""
            UPDATE clinics
            SET beds_available = beds_available + ?
            WHERE name = ?
        """, (num, clinic_name))

        # Commit the changes
        conn.commit()
        print("The availability got increased")
