from rest_framework import serializers
from tracking.models import Employee, LogTime


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class LogtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogTime
        fields = "__all__"
