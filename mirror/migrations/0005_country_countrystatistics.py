# Generated by Django 4.1.3 on 2023-01-17 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mirror', '0004_convertedbeatmapinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('acronym', models.CharField(max_length=2, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('display', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='CountryStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruleset_id', models.IntegerField()),
                ('ranked_score', models.BigIntegerField(default=0)),
                ('play_count', models.BigIntegerField(default=0)),
                ('user_count', models.BigIntegerField(default=0)),
                ('pp', models.BigIntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mirror.country')),
            ],
        ),
    ]