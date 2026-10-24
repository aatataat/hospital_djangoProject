from django.test import TestCase
from django.urls import reverse

from .models import Appointment, Doctor, Patient, Poliklinik


class PoliklinikViewsTests(TestCase):
    def test_poliklinik_list_displays_saved_poliklinik(self):
        Poliklinik.objects.create(nama_poli='Poli Anak', keterangan='Klinik anak')

        response = self.client.get(reverse('poliklinik_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Poli Anak')
        self.assertContains(response, 'Klinik anak')

    def test_poliklinik_create_saves_valid_form(self):
        response = self.client.post(
            reverse('poliklinik_create'),
            {'nama_poli': 'Poli Gigi', 'keterangan': 'Perawatan gigi'},
        )

        self.assertRedirects(response, reverse('poliklinik_list'))
        self.assertTrue(Poliklinik.objects.filter(nama_poli='Poli Gigi').exists())


class PatientViewsTests(TestCase):
    def test_site_root_redirects_to_patient_list(self):
        response = self.client.get('/')

        self.assertRedirects(response, reverse('patient_list'))

    def test_patient_create_saves_valid_form(self):
        response = self.client.post(
            reverse('patient_create'),
            {
                'nomor_rm': 'RM-001',
                'nama_lengkap': 'Budi Santoso',
                'nik': '1234567890123456',
                'tanggal_lahir': '1990-01-02',
                'jenis_kelamin': 'L',
                'alamat': 'Jakarta',
                'no_telepon': '081234567890',
            },
        )

        self.assertRedirects(response, reverse('patient_list'))
        self.assertTrue(Patient.objects.filter(nomor_rm='RM-001').exists())

    def test_patient_list_is_available_at_single_app_prefix(self):
        response = self.client.get(reverse('patient_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('patient_list'), '/patients/')


class AppointmentViewsTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            nomor_rm='RM-001',
            nama_lengkap='Budi Santoso',
            nik='1234567890123456',
            tanggal_lahir='1990-01-02',
            jenis_kelamin='L',
            alamat='Jakarta',
            no_telepon='081234567890',
        )
        self.poliklinik = Poliklinik.objects.create(nama_poli='Poli Umum')
        self.doctor = Doctor.objects.create(
            nama_dokter='Dr. Siti',
            spesialisasi='Umum',
            poliklinik=self.poliklinik,
            no_telepon='081234567891',
        )
        self.appointment = Appointment.objects.create(
            nomor_registrasi='REG-001',
            patient=self.patient,
            doctor=self.doctor,
            tanggal_kunjungan='2026-10-25',
            keluhan='Demam',
        )

    def test_appointment_list_uses_its_own_route(self):
        response = self.client.get(reverse('appointment_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse('appointment_list'), '/appointments/')
        self.assertContains(response, 'REG-001')

    def test_appointment_create_saves_valid_form(self):
        response = self.client.post(
            reverse('appointment_create'),
            {
                'nomor_registrasi': 'REG-002',
                'patient': self.patient.pk,
                'doctor': self.doctor.pk,
                'tanggal_kunjungan': '2026-10-26',
                'keluhan': 'Batuk',
            },
        )

        self.assertRedirects(response, reverse('appointment_list'))
        self.assertTrue(
            Appointment.objects.filter(nomor_registrasi='REG-002').exists()
        )

    def test_appointment_status_update_accepts_valid_choice(self):
        response = self.client.post(
            reverse('appointment_update_status', args=[self.appointment.pk]),
            {'status': 'Diperiksa'},
        )

        self.assertRedirects(response, reverse('appointment_list'))
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'Diperiksa')

    def test_appointment_status_update_rejects_invalid_choice(self):
        response = self.client.post(
            reverse('appointment_update_status', args=[self.appointment.pk]),
            {'status': 'Tidak Valid'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Select a valid choice')
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'Menunggu')
