# Generated by Django 2.1.5 on 2019-01-11 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0025_auto_20190111_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, unique=True),
        ),
    ]
