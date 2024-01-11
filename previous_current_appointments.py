# Importing necessary libraries
import sqlite3
from prettytable import PrettyTable


# Function to display previous appointments of a user
def previous_appointments(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to retrieve all appointments of the user
    cursor.execute('SELECT * FROM appointments WHERE patient_id = ?',
                   (user_id,))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a table to display the appointments
    table = PrettyTable()
    table.field_names = ["Appointment ID", "Status", "Reservation Date",
                         "Payment Amount", "Patient ID", "Clinic ID",
                         "Doctor ID", "Insurance ID", "Payment ID", "Service"]

    # Add each appointment to the table
    for row in rows:
        table.add_row(row)

    # Print the table
    print(table)


# Function to display the current appointment of a user
def current_appointment(user_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()

    # Execute a SQL query to retrieve the latest appointment of the user
    cursor.execute(
        'SELECT * FROM appointments WHERE patient_id = ? ORDER BY patient_id DESC LIMIT 1',
        (user_id,))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Create a table to display the appointment
    table = PrettyTable()
    table.field_names = ["Appointment ID", "Status", "Reservation Date",
                         "Payment Amount", "Patient ID", "Clinic ID",
                         "Doctor ID", "Insurance ID", "Payment ID", "Service"]

    # Add the appointment to the table
    for row in rows:
        table.add_row(row)

    # Print the table
    print(table)
