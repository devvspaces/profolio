# Generated by Django 3.2 on 2022-11-22 00:03

import Account.validators
import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(default=1, help_text='Your Phone number', max_length=20, validators=[Account.validators.validate_phone]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, help_text='Your home address', max_length=200),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, help_text='Your home location', null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(help_text='Enter your full name', max_length=30),
        ),
    ]