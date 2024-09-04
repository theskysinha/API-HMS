# urls.py

from django.urls import path
from .views import (
    index,
    RegisterUser,
    callback,
    login,
    logout,
    DoctorListView,
    doctor_detail,
    PatientListView,
    patient_detail,
    PatientRecordListView,
    patient_record_detail,
    DepartmentListView,
    department_doctors,
    department_patients
)

urlpatterns = [
    path('', index, name='index'),
    path('register', RegisterUser.as_view(), name='register'),
    path('callback', callback, name='callback'),
    path('login', login, name='login'),
    path('logout/', logout, name='logout'),
    path('doctors/', DoctorListView.as_view(), name='doctors_list'),
    path('doctors/<int:pk>/', doctor_detail, name='doctor_detail'),
    path('patients/', PatientListView.as_view(), name='patients_list'),
    path('patient_records/', PatientRecordListView.as_view(), name='patient_records_list'),
    path('patients/<int:pk>/', patient_detail, name='patient_detail'),
    path('patient_records/<int:pk>/', patient_record_detail, name='patient_record_detail'),
    path('departments/', DepartmentListView.as_view(), name='departments_list'),
    path('departments/<int:pk>/doctors/', department_doctors, name='department_doctors'),
    path('departments/<int:pk>/', department_patients, name='department_detail')
]
