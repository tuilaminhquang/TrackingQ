from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    contact = models.CharField(max_length=15, null=True, blank=True)
    salary = models.FloatField(default=22000)
    avatar = models.ImageField(default="default.jpg", upload_to="employee", null=True, blank=True)

    def __str__(self):
        return self.name


class LogTime(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, null=True, related_name="logs"
    )
    date = models.DateTimeField(null=False, blank=False)
    from_hour = models.TimeField(null=False, blank=False)
    to_hour = models.TimeField(null=False, blank=False)
    hour = models.FloatField()

    def __str__(self):
        return f"{self.employee} -- {self.hour} Tiếng"
