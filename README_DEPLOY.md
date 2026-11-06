# Dashboard Integrasi Data Kepegawaian — UI Redesign

## Menjalankan secara lokal

1. Pastikan `hasil.py`, `requirements.txt`, serta folder `03_dataset`, `04_database_operasional`, dan `05_asset` berada di satu direktori (struktur di dalam folder jangan diubah).
2. Gunakan Python 3.11 atau 3.12.
3. Pasang dependensi: `pip install -r requirements.txt`.
4. Konfigurasikan akun melalui Streamlit Secrets (contoh format di bawah), lalu jalankan `streamlit run hasil.py`.

## Streamlit Community Cloud

1. Push seluruh isi folder proyek ini ke repository GitHub, termasuk ketiga folder data/aset dan `requirements.txt`.
2. Buat/deploy aplikasi dengan **Main file path** `hasil.py`.
3. Masukkan bagian `[users]` di **App settings → Secrets** menggunakan akun, password, nama, dan role yang sama dengan konfigurasi existing. Jangan commit password/Secrets ke Git.
4. Restart/redeploy setelah mengubah Secrets.

Contoh struktur Secrets (gunakan nilai akun existing; placeholder ini bukan akun valid):

```toml
[users.admin]
password = "GANTI_DENGAN_PASSWORD_EXISTING"
nama = "Nama Admin Existing"
role = "Admin"

[users.pimpinan]
password = "GANTI_DENGAN_PASSWORD_EXISTING"
nama = "Nama Pimpinan Existing"
role = "Pimpinan"
```

## Tentang perubahan

`hasil.py` adalah turunan langsung dari `app.py` existing. Backend autentikasi, loader, penyimpanan, CRUD, unggah/pemrosesan kehadiran dan KPI, formula, PDF rapor, auto-arsip, struktur kolom, dan rute fungsi bisnis dipertahankan. Navbar menampilkan Dashboard, Data Pegawai, Kehadiran, KPI 7 Aspek ASN, Rapor, dan Arsip; fungsi History Activity tidak lagi dirutekan/ditampilkan sebagai halaman UI. Tombol ubah tema tersedia di navbar. Tambah, Edit, dan Hapus pada Data Pegawai diarahkan ke form CRUD lama (termasuk validasi NIP dan pemindahan ke arsip). Sumber existing tidak menyediakan bulk-import data pegawai; unggah yang memang sudah tersedia untuk Kehadiran dan KPI 7 Aspek tetap memakai proses lama, sedangkan ekspor pegawai tersedia di toolbar. Tidak dibutuhkan file konfigurasi Streamlit tambahan.

Di sumber yang diaudit, nilai role dari Secrets hanya disimpan dan ditampilkan; kode tidak memiliki matriks otorisasi yang membedakan akses Pimpinan dan Admin. Redesign tidak menambahkan atau mengubah permission. Pastikan Secrets deployment tetap memakai identitas dan nilai role existing.

## Catatan persistensi Community Cloud

Aplikasi existing menulis CSV operasional ke direktori lokal proyek. File yang ikut ter-deploy akan tersedia saat aplikasi mulai, tetapi filesystem instance Streamlit Community Cloud bukan penyimpanan permanen; perubahan CSV dapat hilang ketika instance dimulai ulang/redeploy dan tidak cocok untuk beberapa instance yang menulis bersamaan. Ini merupakan batasan backend/deployment existing, bukan perubahan yang diperkenalkan oleh redesign. Untuk penyimpanan jangka panjang perlu storage eksternal/database, yang tidak diubah di paket ini.
