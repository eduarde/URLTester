# Generated by Django 2.1.5 on 2019-01-11 10:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0026_auto_20190111_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='slug',
            field=models.SlugField(blank=True, default=uuid.uuid1, max_length=100, unique=True),
        ),
    ]
