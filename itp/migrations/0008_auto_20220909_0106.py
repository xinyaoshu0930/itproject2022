# Generated by Django 2.1.5 on 2022-09-09 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itp', '0007_auto_20220909_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=300, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='conferenceid',
            field=models.ForeignKey(help_text="<button><a href='add_conference/'>Add A Conference</a></button>", null=True, on_delete=django.db.models.deletion.CASCADE, to='itp.Conference'),
        ),
        migrations.AddField(
            model_name='publication',
            name='tag',
            field=models.ManyToManyField(help_text="<button><a href='add_tag/'>Add A Tag</a></button>", to='itp.Tag'),
        ),
    ]