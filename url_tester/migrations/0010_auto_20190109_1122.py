# Generated by Django 2.1.5 on 2019-01-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0009_auto_20190109_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='code',
        ),
        migrations.AddField(
            model_name='sessionurls',
            name='code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
