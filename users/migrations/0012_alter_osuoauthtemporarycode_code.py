# Generated by Django 4.1.3 on 2023-01-25 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_osuoauthtoken_osuoauthtemporarycode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osuoauthtemporarycode',
            name='code',
            field=models.CharField(max_length=1000),
        ),
    ]
