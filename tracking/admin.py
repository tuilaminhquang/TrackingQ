from django.contrib import admin

# Register your models here.
# admin55 admin

from tracking.models import LogTime, Employee

admin.site.register(Employee)
admin.site.register(LogTime)
