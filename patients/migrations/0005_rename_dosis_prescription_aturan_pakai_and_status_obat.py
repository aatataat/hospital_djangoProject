from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_medicalrecord_prescription'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prescription',
            old_name='dosis',
            new_name='aturan_pakai',
        ),
        migrations.AlterField(
            model_name='prescription',
            name='aturan_pakai',
            field=models.CharField(
                max_length=150,
                verbose_name='Aturan Pakai (Contoh: 3x1 Sesudah Makan)',
            ),
        ),
        migrations.AlterField(
            model_name='prescription',
            name='nama_obat',
            field=models.CharField(
                max_length=150,
                verbose_name='Nama Obat & Dosis',
            ),
        ),
        migrations.AddField(
            model_name='prescription',
            name='status_obat',
            field=models.CharField(
                choices=[('Menunggu', 'Menunggu Pengambilan'), ('Selesai', 'Sudah Diserahkan')],
                default='Menunggu',
                max_length=20,
            ),
        ),
    ]
