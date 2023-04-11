# Generated by Django 4.1.2 on 2023-01-11 17:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "tracking",
            "0002_rename_hour_from_logtime_date_remove_logtime_hour_to_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="logtime",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
