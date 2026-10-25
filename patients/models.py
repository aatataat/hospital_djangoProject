from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ]

    nomor_rm = models.CharField(max_length=20, unique=True, verbose_name="Nomor Rekam Medis")
    nama_lengkap = models.CharField(max_length=100)
    nik = models.CharField(max_length=16, unique=True, verbose_name="NIK")
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES)
    alamat = models.TextField()
    no_telepon = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nomor_rm} - {self.nama_lengkap}"


class Poliklinik(models.Model):
    nama_poli = models.CharField(max_length=100, verbose_name="Nama Poliklinik")
    keterangan = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama_poli

class Doctor(models.Model):
    nama_dokter = models.CharField(max_length=100, verbose_name="Nama Dokter & Gelar")
    spesialisasi = models.CharField(max_length=100)
    poliklinik = models.ForeignKey(Poliklinik, on_delete=models.CASCADE, verbose_name="Poli")
    no_telepon = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.nama_dokter} ({self.spesialisasi})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Menunggu', 'Menunggu'),
        ('Diperiksa', 'Sedang Diperiksa'),
        ('Selesai', 'Selesai'),
        ('Batal', 'Batal'),
    ]

    nomor_registrasi = models.CharField(max_length=20, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Pasien")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="Dokter Tujuan")
    tanggal_kunjungan = models.DateField()
    keluhan = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Menunggu')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nomor_registrasi} - {self.patient.nama_lengkap}"
    

# ------------------------------------------------------------------------------------------------------------------

class MedicalRecord(models.Model):
    # Berelasi 1-ke-1 dengan Appointment atau relasi ke Pasien & Dokter
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, verbose_name="Kunjungan")
    diagnosa = models.TextField(verbose_name="Diagnosa Penyakit")
    tindakan_medis = models.TextField(verbose_name="Tindakan / Terapi")
    catatan_dokter = models.TextField(blank=True, null=True, verbose_name="Catatan Tambahan")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rekam Medis - {self.appointment.patient.nama_lengkap} ({self.created_at.strftime('%d-%m-%Y')})"

class Prescription(models.Model):
    STATUS_RESEP = [
        ('Menunggu', 'Menunggu Pengambilan'),
        ('Selesai', 'Sudah Diserahkan'),
    ]

    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name="prescriptions", verbose_name="Rekam Medis")
    nama_obat = models.CharField(max_length=150, verbose_name="Nama Obat & Dosis")
    jumlah = models.PositiveIntegerField(verbose_name="Jumlah")
    aturan_pakai = models.CharField(max_length=150, verbose_name="Aturan Pakai (Contoh: 3x1 Sesudah Makan)")
    status_obat = models.CharField(max_length=20, choices=STATUS_RESEP, default='Menunggu')

    def __str__(self):
        return f"Resep: {self.nama_obat} ({self.jumlah}) - {self.medical_record.appointment.patient.nama_lengkap}"