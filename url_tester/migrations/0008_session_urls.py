# Generated by Django 2.1.5 on 2019-01-09 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0007_auto_20190109_0925'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='urls',
            field=models.ManyToManyField(related_name='session_url', through='url_tester.SessionURLS', to='url_tester.URL'),
        ),
    ]
