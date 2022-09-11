# Generated by Django 2.1.5 on 2022-09-08 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itp', '0003_auto_20220908_1904'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='publication_author',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='publication_author',
            name='author',
        ),
        migrations.RemoveField(
            model_name='publication_author',
            name='publication',
        ),
        migrations.AddField(
            model_name='publication',
            name='author',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.DeleteModel(
            name='Publication_Author',
        ),
    ]