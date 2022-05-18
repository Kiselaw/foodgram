import csv

from django.core.management.base import BaseCommand

from api.models import Ingredient


def IngredientParser(file):
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            new_ingredient = Ingredient(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
            new_ingredient.save()


COMMANDS = {
    'ingredient': IngredientParser,
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        for key in COMMANDS.keys():
            parser.add_argument(f'--{key}', type=str)

    def handle(self, *args, **options):
        for key, parser in COMMANDS.items():
            if options[key]:
                file_path = options[key]
                parser(file_path)
                self.stdout.write(self.style.SUCCESS(
                    f'{key.capitalize()}s successfully '
                    f'added from file {file_path}'))
