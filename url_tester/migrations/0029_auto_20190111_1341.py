# Generated by Django 2.1.5 on 2019-01-11 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0028_project_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='color',
            field=models.CharField(blank=True, max_length=7, null=True, verbose_name='Color Code'),
        ),
    ]