import csv
import datetime
from pathlib import Path

data_folder = Path(__file__).parent.parent
hospital_details_path = data_folder / "Hospital-Details.csv"
hospital_departments_path = data_folder / "Hospital-Departments.csv"
hospital_on_duty_path = data_folder / "On-duty-May-2020.csv"


def get_hospital_details(Hospital, data_path=hospital_details_path):
    with open(data_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [Hospital(**row) for row in reader]


def get_hospital_departments(Department, data_path=hospital_departments_path):
    with open(data_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        return [Department(**row) for row in reader]


def get_on_duty(OnDuty, data_path=hospital_on_duty_path):
    def to_date(text):
        day, month, year = [int(date_part) for date_part in text.split("/")]
        return datetime.date(year, month, day)

    with open(data_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file, delimiter=";")
        mapped_dates = [{**row, "date": to_date(row["date"])} for row in reader]
        return [OnDuty(**row) for row in mapped_dates]
