import sqlite3
from prettytable import PrettyTable
conn = sqlite3.connect('ap_database.db')
c = conn.cursor()


def manoeuvre(request):
    if request == 1:
        doc = input('Would you like to view the appointments for a specific doctor? If so, please enter his/her id. Otherwise, I can display all appointments.(Please enter all)')
        hosp = input('Would you like to view the appointments for a specific hospital? If so, please enter its id. Otherwise, I can display all appointments.(Please enter all)')
        if doc == 'all' and hosp == 'all':
            c.execute("SELECT * FROM appointments")
            results = c.fetchall()
            for res in results:
                print(res)
        elif doc != 'all' and hosp =='all':
            doc = int(doc)
            c.execute('SELECT * FROM appointments WHERE doctor_id = ?', (doc,))
            results = c.fetchall()
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]
            for row in results:
                table.add_row(row)
            print(table)
        elif doc == 'all' and hosp != 'all':
            hosp = int(hosp)
            c.execute('SELECT * FROM appointments WHERE clinic_id = ?', (hosp,))
            results = c.fetchall()
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date", "Payment Amount", "Patient ID", "Clinic ID", "Doctor ID", "Insurance ID", "Payment ID", "Service"]
            for row in results:
                table.add_row(row)
            print(table)
        else:
            doc = int(doc)
            hosp = int(hosp)
            c.execute('SELECT * FROM appointments WHERE doctor_id = ? AND clinic_id = ?', (doc, hosp))
            results = c.fetchall()
            table = PrettyTable()
            table.field_names = ["Appointment ID", "Status", "Reservation Date",
                                 "Payment Amount", "Patient ID", "Clinic ID",
                                 "Doctor ID", "Insurance ID", "Payment ID",
                                 "Service"]
            for row in results:
                table.add_row(row)
            print(table)
    elif request == 2:
        id = input('Please enter ID of the appointment which you wish to delete')
        c.execute(
            'DELETE FROM appointments WHERE appointment_id = ?', (id)
        )
        conn.commit()
    elif request == 3:
        clinic_name = input('Please enter the name of the clinic for which you wish to increase the number of available beds.')
        num = int(input('How many more beds?'))
        c.execute("""
            UPDATE clinics
            SET beds_available = beds_available + ?
            WHERE name = ?
        """, (num, clinic_name))
        conn.commit()
