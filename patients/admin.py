from django.contrib import admin
from .models import Patient, Poliklinik, Doctor, MedicalRecord, Prescription

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('nomor_rm', 'nik', 'nama_lengkap', 'jenis_kelamin', 'no_telepon')
    search_fields = ('nomor_rm', 'nik', 'nama_lengkap')

admin.site.register(Poliklinik)
admin.site.register(Doctor)
admin.site.register(MedicalRecord)
admin.site.register(Prescription)