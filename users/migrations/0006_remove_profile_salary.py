# Generated by Django 4.1.2 on 2023-01-20 03:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_profile_salary"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="salary",
        ),
    ]
