# Generated by Django 4.2.4 on 2023-08-09 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='created_at',
            new_name='created_time',
        ),
    ]
