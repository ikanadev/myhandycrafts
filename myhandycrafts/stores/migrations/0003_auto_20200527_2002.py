# Generated by Django 2.2.10 on 2020-05-28 00:02

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_store_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='gps',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
