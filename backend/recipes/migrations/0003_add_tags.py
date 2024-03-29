# Generated by Django 2.2.16 on 2022-12-14 11:44

from django.db import migrations

TAGS = [
    {'color_code': '#800080', 'name': 'Ужин', 'slug': 'dinner'},  # purple
    {'color_code': '#008000', 'name': 'Обед', 'slug': 'lunch'},  # green
    {'color_code': '#FF8C00', 'name': 'Завтрак', 'slug': 'breakfast'}  # orange
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in TAGS:
        new_tag = Tag(**tag)
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    for tag in TAGS:
        Tag.objects.get(slug=tag['slug']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20221214_1442'),
    ]

    operations = [
        migrations.RunPython(add_tags, remove_tags)
    ]
