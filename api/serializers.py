# serializers.py

from rest_framework import serializers
from .models import User, PatientRecord, Department

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'role', 'department']
        
class PatientRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientRecord
        fields = ['record_id', 'patient', 'created_date', 'diagnostics', 'observations', 'treatments', 'department', 'misc']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'diagnostics', 'location', 'specialization']
