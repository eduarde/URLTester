# Generated by Django 2.1.5 on 2019-01-10 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0016_session_loaded'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='type',
            field=models.CharField(blank=True, max_length=400, null=True, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='session',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='session',
            name='title',
            field=models.CharField(max_length=400, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='session',
            name='url_load',
            field=models.URLField(blank=True, null=True, verbose_name='URL to load'),
        ),
    ]