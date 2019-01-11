# Generated by Django 2.1.5 on 2019-01-11 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_tester', '0030_auto_20190111_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='color',
            field=models.CharField(blank=True, help_text='Add the desired color code. You can choose one from <a href="http://brand-colors.com/" target="_blank">here</a>', max_length=7, null=True, verbose_name='Color Code'),
        ),
    ]
