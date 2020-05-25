import csv
import datetime
from pathlib import Path

from .db import db, Region, Hospital, Department, HasDepartment, OnDuty

data_folder = Path(__file__).parent.parent
regions_path = data_folder / "Regions.csv"
hospitals_path = data_folder / "Hospitals.csv"
departments_path = data_folder / "Departments.csv"
hospital_departments_path = data_folder / "Hospital-Departments.csv"
hospital_on_duty_path = data_folder / "On-duty.csv"


def get_regions(data_path=regions_path):
    with open(str(data_path), newline="", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [Region(**row) for row in reader]


def get_hospitals(data_path=hospitals_path):
    with open(str(data_path), newline="", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [Hospital(**row) for row in reader]


def get_departments(data_path=departments_path):
    with open(str(data_path), newline="", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [Department(**row) for row in reader]


def get_hospital_departments(data_path=hospital_departments_path):
    with open(str(data_path), newline="", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [HasDepartment(**row) for row in reader]


def get_on_duty(data_path=hospital_on_duty_path):
    def to_date(text):
        day, month, year = [int(date_part) for date_part in text.split("/")]
        return datetime.date(year, month, day)

    with open(str(data_path), newline="", encoding="utf8") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        mapped_dates = [{**row, "date": to_date(row["date"])} for row in reader]
        return [OnDuty(**row) for row in mapped_dates]


def load_data():
    db.session.bulk_save_objects(get_regions())
    db.session.bulk_save_objects(get_hospitals())
    db.session.bulk_save_objects(get_departments())
    db.session.bulk_save_objects(get_hospital_departments())
    db.session.bulk_save_objects(get_on_duty())
    db.session.commit()
