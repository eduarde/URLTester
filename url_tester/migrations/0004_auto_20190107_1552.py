# Generated by Django 2.1.5 on 2019-01-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0003_auto_20190107_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
