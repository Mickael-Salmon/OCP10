# Generated by Django 4.2.4 on 2023-11-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userconsent_date_of_birth'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userconsent',
            name='date_of_birth',
        ),
    ]