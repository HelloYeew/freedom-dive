# Generated by Django 4.1.3 on 2023-01-25 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_osuoauthtemporarycode_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osuoauthtoken',
            name='access_token',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='osuoauthtoken',
            name='refresh_token',
            field=models.CharField(max_length=1000),
        ),
    ]
