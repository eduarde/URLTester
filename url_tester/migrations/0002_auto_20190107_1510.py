# Generated by Django 2.1.5 on 2019-01-07 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='run_date',
            new_name='date',
        ),
    ]
