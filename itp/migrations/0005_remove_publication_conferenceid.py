# Generated by Django 2.1.5 on 2022-09-08 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('itp', '0004_auto_20220908_2022'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='conferenceid',
        ),
    ]