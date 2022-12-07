# Generated by Django 2.2.16 on 2022-12-07 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
        ('users', '0002_add_User_and_Follow'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(related_name='user_favorites', to='recipes.Recipe', verbose_name='Избранные рецепты'),
        ),
    ]
