# Generated by Django 3.2.9 on 2021-11-22 01:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0003_auto_20211120_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='password',
        ),
    ]
