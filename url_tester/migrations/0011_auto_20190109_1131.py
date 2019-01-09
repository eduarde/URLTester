# Generated by Django 2.1.5 on 2019-01-09 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0010_auto_20190109_1122'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='urls',
        ),
        migrations.AddField(
            model_name='session',
            name='urls',
            field=models.ManyToManyField(blank=True, null=True, related_name='session_url', to='url_tester.URL'),
        ),
    ]
