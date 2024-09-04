# views.py

import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication
from .models import PatientRecord, User, Department
from .serializers import UserSerializer, PatientRecordSerializer, DepartmentSerializer
from datetime import datetime

# Initialize OAuth
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

class RegisterUser(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        print(data)
        if 'department' in data:
            try:
                department_id = Department.objects.get(id=data['department'])
            except Department.DoesNotExist:
                return Response({"error": "Department does not exist"}, status=404)
        
        user = User.objects.create(
            email=data['email'],
            name=data['name'],
            password=data['password'],
            role=data['role'],
            department=department_id
        )
        user.save()
        return Response(UserSerializer(user).data)

# Auth0 Authentication Views
def index(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(reverse("login"))

@api_view(['GET'])
@authentication_classes([SessionAuthentication])
def login(request):
    if not request.session.get("user"):
        return redirect(reverse("index"))
        
    data = request.session.get("user")
    
    return Response(data)
    

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

# Doctor Views class based

class DoctorListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(role='doctor')

    def get(self, request):
        doctors = User.objects.filter(role='doctor')
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        doctor = User.objects.create(
            email=data['email'],
            name=data['name'],
            password=data['password'],
            role='doctor',
            department=data['department']
        )
        doctor.save()
        return Response(UserSerializer(doctor).data)
   

@api_view(['GET', 'PUT', 'DELETE'])
def doctor_detail(request, pk):
    try:
        doctor = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(doctor)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        doctor.email = data['email']
        doctor.name = data['name']
        doctor.password = data['password']
        doctor.save()
        return Response(UserSerializer(doctor).data)
    
    elif request.method == 'DELETE':
        doctor.delete()
        return Response(status=204)
    

class PatientListView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.filter(role='patient')

    def get(self, request):
        patients = User.objects.filter(role='patient')
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        
        if 'department' in data:
            try:
                department_id = Department.objects.get(id=data['department'])
            except Department.DoesNotExist:
                return Response({"error": "Department does not exist"}, status=404)
        
        patient = User.objects.create(
            email=data['email'],
            name=data['name'],
            password=data['password'],
            role='patient',
            department=department_id
        )
        patient.save()
        return Response(UserSerializer(patient).data)
    
@api_view(['GET', 'PUT', 'DELETE'])
def patient_detail(request, pk):
    try:
        patient = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = UserSerializer(patient)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        patient.email = data['email']
        patient.name = data['name']
        patient.password = data['password']
        patient.save()
        return Response(UserSerializer(patient).data)
    
    elif request.method == 'DELETE':
        patient.delete()
        return Response(status=204)

# PatientRecord Views
class PatientRecordListView(generics.ListAPIView):
    serializer_class = PatientRecordSerializer
    queryset = PatientRecord.objects.all()

    def get(self, request):
        patient_records = PatientRecord.objects.all()
        serializer = PatientRecordSerializer(patient_records, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        
        if 'department' in data:
            try:
                department_id = Department.objects.get(id=data['department'])
            except Department.DoesNotExist:
                return Response({"error": "Department does not exist"}, status=404)
        
        patient_record = PatientRecord.objects.create(
            patient= data['patient'],
            department=department_id,
            observations=data['observations'],
            treatments=data['treatments'],
            created_date=datetime.now(),
            diagnostics=data['diagnostics'],
            misc=data['misc']
        )
        patient_record.save()
        return Response(PatientRecordSerializer(patient_record).data)

@api_view(['GET', 'PUT', 'DELETE'])
def patient_record_detail(request, pk):
    try:
        patient_record = PatientRecord.objects.get(pk=pk)
    except PatientRecord.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        serializer = PatientRecordSerializer(patient_record)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        patient_record.patient_id = data['patient_id']
        patient_record.doctor_id = data['doctor_id']
        patient_record.department_id = data['department_id']
        patient_record.date = data['date']
        patient_record.diagnosis = data['diagnosis']
        patient_record.prescription = data['prescription']
        patient_record.save()
        return Response(PatientRecordSerializer(patient_record).data)
    
    elif request.method == 'DELETE':
        patient_record.delete()
        return Response(status=204)
    
# Department Views
class DepartmentListView(generics.ListAPIView):
    serializer_class = DepartmentSerializer
    queryset = Department.objects.all()

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        department = Department.objects.create(
            name=data['name'],
            diagnostics=data['diagnostics'],
            location=data['location'],
            specialization=data['specialization']
        )
        department.save()
        return Response(DepartmentSerializer(department).data)
    
@api_view(['GET', 'PUT'])
def department_doctors(request, pk):
    try:
        department = Department.objects.get(pk=pk)
        user = User.objects.get(role='doctor')
    except Department.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        doctors = User.objects.filter(role='doctor', department=department)
        serializer = UserSerializer(doctors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']
        user.role = 'doctor'
        user.department = data['department']
        user.save()
        return Response(DepartmentSerializer(department).data)
    
@api_view(['GET', 'PUT'])
def department_patients(request, pk):
    try:
        department = Department.objects.get(pk=pk)
        user = User.objects.get(role='patient')
    except Department.DoesNotExist:
        return Response(status=404)
    
    if request.method == 'GET':
        patients = User.objects.filter(role='patient', department=department)
        serializer = UserSerializer(patients, many=True)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        user.name = data['name']
        user.email = data['email']
        user.password = data['password']
        user.role = 'patient'
        user.department = data['department']
        user.save()
        return Response(DepartmentSerializer(department).data)