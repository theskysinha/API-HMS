# models.py

from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    diagnostics = models.TextField()
    location = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PatientRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    diagnostics = models.TextField()
    observations = models.TextField()
    treatments = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    misc = models.TextField()

    def __str__(self):
        return f"Record {self.record_id} for {self.patient.user.username}"

#make a user model with fields like email, name, password, role = Doctor, Patient
class User(models.Model):
    email = models.EmailField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name