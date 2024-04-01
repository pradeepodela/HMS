import streamlit as st
import sqlite3
from datetime import date

class Doctor:
    def __init__(self, name, surname, age, specialty, salary):
        self.name = name
        self.surname = surname
        self.age = age
        self.specialty = specialty
        self.salary = salary

    def show_info(self):
        st.write(f"""
            Name: {self.name}
            Surname: {self.surname}
            Age: {self.age}
            Specialty: {self.specialty}
            Salary: {self.salary}
        """)

class Nurse:
    def __init__(self, name, surname, age, unit, salary):
        self.name = name
        self.surname = surname
        self.age = age
        self.unit = unit
        self.salary = salary

    def show_info(self):
        st.write(f"""
            Name: {self.name}
            Surname: {self.surname}
            Age: {self.age}
            Unit: {self.unit}
            Salary: {self.salary}
        """)

class Patient:
    def __init__(self, name, surname, id, date_of_birth, sickness):
        self.name = name
        self.surname = surname
        self.id = id
        self.date_of_birth = date_of_birth
        self.sickness = sickness
        self.bill = 0
        self.is_here = None

    def show_info(self):
        st.write("Patient Info:")
        st.write(f"""
            Name: {self.name}
            Surname: {self.surname}
            ID: {self.id}
            Date Of Birth: {self.date_of_birth}
        """)

class HospitalControlPanel:
    def __init__(self):
        self.db = "HospitalControlPanel.db"
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS PATIENT(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(50),
                SURNAME VARCHAR(50),
                IDENTITY_ VARCHAR(11),
                DATEOFBIRTH DATE,
                SICKNESS VARCHAR(50)
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NURSE(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(50),
                SURNAME VARCHAR(50),
                AGE VARCHAR(3),
                UNIT VARCHAR(30),
                SALARY INTEGER
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS DOCTOR(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NAME VARCHAR(50),
                SURNAME VARCHAR(50),
                AGE VARCHAR(3),
                SPECIALTY VARCHAR(40),
                SALARY INTEGER
            )
        """)

    def add_doctor(self, name, surname, age, specialty, salary):
        try:
            doctor = Doctor(name, surname, age, specialty, salary)
            self.cursor.execute("INSERT INTO DOCTOR (NAME, SURNAME, AGE, SPECIALTY, SALARY) VALUES (?,?,?,?,?)",
                                (doctor.name, doctor.surname, doctor.age, doctor.specialty, doctor.salary))
            self.conn.commit()
            st.write(f"{doctor.name} {doctor.surname} added to the system")
        except ValueError:
            st.write("Please write a numerical data for the salary and try again.")

    def add_nurse(self, name, surname, age, unit, salary):
        try:
            nurse = Nurse(name, surname, age, unit, salary)
            self.cursor.execute("INSERT INTO NURSE (NAME, SURNAME, AGE, UNIT, SALARY) VALUES (?,?,?,?,?)",
                                (nurse.name, nurse.surname, nurse.age, nurse.unit, nurse.salary))
            self.conn.commit()
            st.write(f"{nurse.name} {nurse.surname} added to the system.")
        except ValueError:
            st.write("Please write a numerical data for the salary and try again.")

    def sign_patient(self, name, surname, id, date_of_birth, sickness):
        patient = Patient(name, surname, id, date_of_birth, sickness)
        self.cursor.execute("INSERT INTO PATIENT (NAME, SURNAME, IDENTITY_,DATEOFBIRTH, SICKNESS) VALUES(?,?,?,?,?)",
                             (patient.name, patient.surname, patient.id, patient.date_of_birth, patient.sickness))
        self.conn.commit()
        st.write(f"{patient.name} {patient.surname} added to the system.")

    # Methods for deleting nurses, doctors, patients, etc. go here

    def show_all_patients(self):
        self.cursor.execute("SELECT * FROM PATIENT")
        patients = self.cursor.fetchall()
        if not patients:
            st.write("There are no patients in the hospital.")
        else:
            st.write("\nPatients:")
            for patient in patients:
                patient_obj = Patient(*patient[1:])
                patient_obj.show_info()

    def show_all_nurses(self):
        self.cursor.execute("SELECT * FROM NURSE")
        nurses = self.cursor.fetchall()
        if not nurses:
            st.write("There are no nurses in the hospital.")
        else:
            st.write("\nNurses:")
            for nurse in nurses:
                nurse_obj = Nurse(*nurse[1:])
                nurse_obj.show_info()

    def show_all_doctors(self):
        self.cursor.execute("SELECT * FROM DOCTOR")
        doctors = self.cursor.fetchall()
        if not doctors:
            st.write("There are no doctors in the hospital.")
        else:
            st.write("\nDoctors:")
            for doctor in doctors:
                doctor_obj = Doctor(*doctor[1:])
                doctor_obj.show_info()

def main():
    hospital = HospitalControlPanel()
    hospital.create_tables()
    st.title("Hospital Management Panel")
    proc = st.selectbox("Select Process:", [
        "Sign Patient",
        "Add Nurse",
        "Add Doctor",
        "Show All Patients",
        "Show All Nurses",
        "Show All Doctors"
    ])
    if proc == "Sign Patient":
        name = st.text_input("Name:")
        surname = st.text_input("Surname:")
        id = st.text_input("ID:")
        date_of_birth = st.text_input("Date Of Birth (YYYY-MM-DD):")
        sickness = st.text_input("Sickness:")
        if st.button("Sign"):
            hospital.sign_patient(name, surname, id, date_of_birth, sickness)
    elif proc == "Add Nurse":
        name = st.text_input("Name:")
        surname = st.text_input("Surname:")
        age = st.text_input("Age:")
        unit = st.text_input("Unit:")
        salary = st.text_input("Salary:")
        if st.button("Add"):
            hospital.add_nurse(name, surname, age, unit, salary)
    elif proc == "Add Doctor":
        name = st.text_input("Name:")
        surname = st.text_input("Surname:")
        age = st.text_input("Age:")
        specialty = st.text_input("Specialty:")
        salary = st.text_input("Salary:")
        if st.button("Add"):
            hospital.add_doctor(name, surname, age, specialty, salary)
    elif proc == "Show All Patients":
        hospital.show_all_patients()
    elif proc == "Show All Nurses":
        hospital.show_all_nurses()
    elif proc == "Show All Doctors":
        hospital.show_all_doctors()


main()
