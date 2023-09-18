import csv
from datetime import datetime
from random import randint
from faker import Faker
from django.core.management.base import BaseCommand
from scoring.models import Client

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Client model'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        fake = Faker()
        file_path = options['file_path']
        with open(file_path, 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                iin = self.generate_iin(row['age'])
                name = self.generate_fake_name(fake)
                data = {
                    'iin': iin,
                    'name': name,
                    'status': row['status'],
                    'duration': int(row['duration']),
                    'credit_history': row['credit_history'],
                    'purpose': row['purpose'],
                    'amount': int(row['amount']),
                    'savings': row['savings'],
                    'employment_duration': row['employment_duration'],
                    'installment_rate': row['installment_rate'],
                    'personal_status_sex': row['personal_status_sex'],
                    'property': row['property'],
                    'age': int(row['age']),
                    'number_credits': row['number_credits'],
                    'job': row['job'],
                    'people_liable': int(row['people_liable']),
                    'telephone': row['telephone'],
                    'credit_risk': int(row['credit_risk']),
                }
                self.create_model_instance(data)

    def generate_iin(self, age):
        birth_date = datetime.now().replace(year=datetime.now().year - int(age))
        iin = birth_date.strftime('%y%m%d') + str(randint(100000, 999999))
        return iin

    def generate_fake_name(self, fake):
        name = fake.first_name()
        surname = fake.last_name()
        return f'{name} {surname}'

    def create_model_instance(self, data):
        model_instance = Client(**data)
        model_instance.save()
