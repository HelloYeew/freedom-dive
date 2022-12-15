# Generated by Django 4.1.3 on 2022-12-15 07:29

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_scorestore_statistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientChangelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('content', martor.models.MartorField()),
            ],
        ),
    ]