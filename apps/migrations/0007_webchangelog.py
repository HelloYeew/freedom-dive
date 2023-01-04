# Generated by Django 4.1.3 on 2022-12-22 18:40

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0006_clientchangelog_download_url_linux_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebChangelog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('public', models.BooleanField(default=False)),
                ('content', mdeditor.fields.MDTextField(blank=True, null=True)),
            ],
        ),
    ]