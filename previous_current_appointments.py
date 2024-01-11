import sqlite3
from prettytable import PrettyTable


def previous_appointments(user_id):
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments WHERE patient_id = ?',
                   (user_id,))
    rows = cursor.fetchall()
    conn.close()
    table = PrettyTable()
    table.field_names = ["Appointment ID", "Status", "Reservation Date",
                         "Payment Amount", "Patient ID", "Clinic ID",
                         "Doctor ID", "Insurance ID", "Payment ID", "Service"]
    for row in rows:
        table.add_row(row)
    print(table)


def current_appointment(user_id):
    conn = sqlite3.connect('ap_database.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM appointments WHERE patient_id = ? ORDER BY patient_id DESC LIMIT 1',
        (user_id,))
    rows = cursor.fetchall()
    conn.close()
    table = PrettyTable()
    table.field_names = ["Appointment ID", "Status", "Reservation Date",
                         "Payment Amount", "Patient ID", "Clinic ID",
                         "Doctor ID", "Insurance ID", "Payment ID", "Service"]
    for row in rows:
        table.add_row(row)
    print(table)
