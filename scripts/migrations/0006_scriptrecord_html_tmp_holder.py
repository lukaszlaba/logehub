# Generated by Django 3.1.5 on 2021-02-11 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scripts', '0005_scriptrecord_last_time_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='scriptrecord',
            name='html_tmp_holder',
            field=models.TextField(default='None'),
        ),
    ]
