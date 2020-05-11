# Generated by Django 2.2.10 on 2020-05-11 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200508_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='deleted_at',
            field=models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at'),
        ),
        migrations.AlterField(
            model_name='postmedia',
            name='deleted_at',
            field=models.DateTimeField(help_text='Date time on which the objects was deleted.', null=True, verbose_name='deleted_at'),
        ),
    ]
