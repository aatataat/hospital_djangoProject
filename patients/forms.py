from django import forms
from .models import Appointment, MedicalRecord, Patient, Poliklinik

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['nomor_rm', 'nama_lengkap', 'nik', 'tanggal_lahir', 'jenis_kelamin', 'alamat', 'no_telepon']
        widgets = {
            'nomor_rm': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: RM-001'}),
            'nama_lengkap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap pasien'}),
            'nik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '16 digit NIK'}),
            'tanggal_lahir': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'alamat': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alamat lengkap'}),
            'no_telepon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['nomor_registrasi', 'patient', 'doctor', 'tanggal_kunjungan', 'keluhan']
        widgets = {
            'nomor_registrasi': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'REG-001'}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'tanggal_kunjungan': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'keluhan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Keluhan pasien...'}),
        }


class AppointmentStatusForm(forms.Form):
    status = forms.ChoiceField(
        choices=Appointment.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Pilih Status Terbaru',
    )


class PoliklinikForm(forms.ModelForm):
    class Meta:
        model = Poliklinik
        fields = ['nama_poli', 'keterangan']
        widgets = {
            'nama_poli': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Poliklinik'}),
            'keterangan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Keterangan tambahan (opsional)'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['appointment', 'diagnosa', 'tindakan_medis', 'catatan_dokter']
        widgets = {
            'appointment': forms.Select(attrs={'class': 'form-select'}),
            'diagnosa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Masukkan hasil diagnosa...'}),
            'tindakan_medis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tindakan atau resep terapi...'}),
            'catatan_dokter': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Catatan khusus (opsional)...'}),
        }