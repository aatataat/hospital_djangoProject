from django.urls import path
from .views import (
    patient_list, patient_create, 
    appointment_list, appointment_create, 
    appointment_update_status,
    poliklinik_list, poliklinik_create,
    medical_record_list, medical_record_create,
)

urlpatterns = [
    path('patients/', patient_list, name='patient_list'),
    path('patients/add/', patient_create, name='patient_create'),
    path('appointments/', appointment_list, name='appointment_list'),
    path('appointments/add/', appointment_create, name='appointment_create'),
    path('appointments/update/<int:pk>/', appointment_update_status, name='appointment_update_status'),
    path('poliklinik/', poliklinik_list, name='poliklinik_list'),
    path('poliklinik/add/', poliklinik_create, name='poliklinik_create'),
    path('medical-records/', medical_record_list, name='medical_record_list'),
    path('medical-records/add/', medical_record_create, name='medical_record_create'),
]
