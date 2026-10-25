from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render

from .models import Appointment, Patient, Poliklinik, MedicalRecord, Prescription

from .forms import (
    AppointmentForm,
    AppointmentStatusForm,
    PatientForm,
    PoliklinikForm,
    MedicalRecordForm,
    PrescriptionForm,
)

def patient_list(request):
    patients = Patient.objects.all().order_by('nama_lengkap', 'id')
    context = {'patients': patients}
    return render(request, 'patients/patient_list.html', context)

# Fungsi tambah data pasien baru
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save() # Menyimpan data ke database (mirip Patient::create())
            return redirect('patient_list') # Redirect ke halaman daftar pasien
    else:
        form = PatientForm()
    
    context = {'form': form}
    return render(request, 'patients/patient_form.html', context)


def poliklinik_list(request):
    polikliniks = Poliklinik.objects.all().order_by('nama_poli')
    return render(request, 'patients/poliklinik_list.html', {'polikliniks': polikliniks})


def poliklinik_create(request):
    if request.method == 'POST':
        form = PoliklinikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('poliklinik_list')
    else:
        form = PoliklinikForm()

    return render(request, 'patients/poliklinik_form.html', {'form': form})


# Fungsi menampilkan daftar kunjungan/pendaftaran poli
def appointment_list(request):
    appointments = (
        Appointment.objects.select_related('patient', 'doctor__poliklinik')
        .order_by('-created_at')
    )
    context = {'appointments': appointments}
    return render(request, 'patients/appointment_list.html', context)

# Fungsi tambah pendaftaran poli
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    
    context = {'form': form}
    return render(request, 'patients/appointment_form.html', context)

def appointment_update_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST)
        if form.is_valid():
            appointment.status = form.cleaned_data['status']
            appointment.save(update_fields=['status'])
            return redirect('appointment_list')
    else:
        form = AppointmentStatusForm(initial={'status': appointment.status})

    context = {'appointment': appointment, 'form': form}
    return render(request, 'patients/appointment_update.html', context)


def medical_record_list(request):
    records = MedicalRecord.objects.all().order_by('-created_at')
    context = {'records': records}
    return render(request, 'patients/medical_record_list.html', context)

def medical_record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save()
            # Otomatis ubah status appointment menjadi 'Selesai' jika rekam medis sudah diisi
            record.appointment.status = 'Selesai'
            record.appointment.save()
            return redirect('medical_record_list')
    else:
        form = MedicalRecordForm()
    
    context = {'form': form}
    return render(request, 'patients/medical_record_form.html', context)




def prescription_list(request):
    prescriptions = Prescription.objects.all().order_by('-id')
    context = {'prescriptions': prescriptions}
    return render(request, 'patients/prescription_list.html', context)

def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescription_list')
    else:
        form = PrescriptionForm()
    
    context = {'form': form}
    return render(request, 'patients/prescription_form.html', context)