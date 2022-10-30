import csv
from pathlib import Path
from backend.settings import BASE_DIR

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from recipes.models import Ingredient

User = get_user_model()

PROJECT_DIR = Path(BASE_DIR).resolve().joinpath('data')
FILE_TO_OPEN = PROJECT_DIR / 'ingredients.csv'


class Command(BaseCommand):
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **options):
        with open(
            FILE_TO_OPEN,
            'r',
            encoding='utf-8'
        ) as csvfile:
            order = ['name', 'measurement_unit']
            data_reader = csv.DictReader(
                csvfile,
                fieldnames=order,
                delimiter=',')
            Ingredient.objects.bulk_create([Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            ) for row in data_reader])
