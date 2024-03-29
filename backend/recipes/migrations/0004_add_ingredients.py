# Generated by Django 2.2.16 on 2022-12-14 11:46

import csv
import os

from django.db import migrations

from foodgram.settings import BASE_DIR

ROOT_DIR = os.path.dirname(BASE_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data/')
INGREDIENT_FILE = 'ingredients.csv'


def get_ingredients():
    result = []
    file_path = os.path.join(DATA_DIR, INGREDIENT_FILE)
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append({'name': row[0], 'measurement_unit': row[1]})
    except FileNotFoundError:
        print('Файл с данными отсутствует.')
    return result


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    ingredients = get_ingredients()
    for ingredient in ingredients:
        new_item = Ingredient(**ingredient)
        new_item.save()


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipes', 'Ingredient')
    ingredients = get_ingredients()
    for ingredient in ingredients:
        Ingredient.objects.get(name=ingredient['name']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_add_tags'),
    ]

    operations = [
        migrations.RunPython(add_ingredients, remove_ingredients)
    ]
