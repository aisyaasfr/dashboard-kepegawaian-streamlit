from pathlib import Path
from datetime import date, datetime, timedelta
import random
import calendar
import pandas as pd

# =========================================================
# KONFIGURASI
# =========================================================
random.seed(2026)

BASE = Path(__file__).resolve().parent
DATASET = BASE / "03_dataset" / "employee"
DB = BASE / "04_database_operasional"

DATASET.mkdir(parents=True, exist_ok=True)
(DB / "employee").mkdir(parents=True, exist_ok=True)
(DB / "attendance").mkdir(parents=True, exist_ok=True)
(DB / "performance").mkdir(parents=True, exist_ok=True)

START = date(2026, 1, 1)
END = date(2026, 4, 30)

# =========================================================
# REFERENSI DATA FIKTIF
# =========================================================
nama_depan = [
    "Aditya", "Aulia", "Bagas", "Citra", "Dimas",
    "Dewi", "Fajar", "Farah", "Galih", "Intan",
    "Rizky", "Nadia", "Raka", "Salsabila", "Bima",
    "Putri", "Rafi", "Nabila", "Yoga", "Anindya"
]

nama_belakang = [
    "Pratama", "Nugraha", "Saputra", "Permata", "Wijaya",
    "Kusuma", "Pangestu", "Ramadhan", "Lestari", "Puspita",
    "Mahendra", "Wulandari", "Firmansyah", "Anggraini",
    "Kurniawan", "Oktaviani", "Setiawan", "Maulana",
    "Handayani", "Prameswari"
]

unit_kerja = [
    "Sekretariat Daerah",
    "Badan Kepegawaian",
    "Dinas Pendidikan",
    "Dinas Kesehatan",
    "Dinas Komunikasi dan Informatika",
    "Dinas Perhubungan",
    "Dinas Sosial",
    "Badan Perencanaan Daerah",
    "Dinas Lingkungan Hidup",
    "Badan Keuangan Daerah"
]

jabatan = [
    "Analis Kepegawaian",
    "Analis Data",
    "Pengelola Administrasi",
    "Pranata Komputer",
    "Analis Perencanaan",
    "Pengelola Keuangan",
    "Pengadministrasi Umum",
    "Analis Kebijakan"
]

jenjang = ["SMA", "D3", "S1", "S2"]
golongan = ["II/a", "II/c", "III/a", "III/b", "III/c", "IV/a"]

# Kombinasi nama dibuat unik
semua_nama = [
    f"{depan} {belakang}"
    for depan in nama_depan
    for belakang in nama_belakang
]
random.shuffle(semua_nama)

def tambah_tahun(tanggal, tahun):
    try:
        return tanggal.replace(year=tanggal.year + tahun)
    except ValueError:
        return tanggal.replace(year=tanggal.year + tahun, day=28)

def buat_pegawai(no, arsip=False):
    nama = semua_nama[no - 1]
    jk = random.choice(["L", "P"])
    tahun_lahir = random.randint(1962, 1967) if arsip else random.randint(1970, 2000)
    lahir = date(tahun_lahir, random.randint(1, 12), random.randint(1, 28))
    usia = END.year - lahir.year - ((END.month, END.day) < (lahir.month, lahir.day))

    tmt_masuk = tambah_tahun(lahir, 22)
    if tmt_masuk > END:
        tmt_masuk = date(2020, 1, 1)

    tmt_pangkat = min(tambah_tahun(tmt_masuk, random.randint(1, 6)), END)
    tmt_pensiun = tambah_tahun(lahir, 58)

    nip = f"99999999{no:010d}"
    nik = f"999999999999{no:04d}"

    return {
        "NO": no,
        "NAMA": nama,
        "NIP BARU": nip,
        "NIK": nik,
        "JK": jk,
        "AGAMA": random.choice(["Islam", "Kristen", "Katolik", "Hindu", "Buddha"]),
        "STATUS PNS/CPNS": "PNS",
        "JENJANG": random.choice(jenjang),
        "NAMA JABATAN": random.choice(jabatan),
        "UNIT KERJA": random.choice(unit_kerja),
        "TGL LAHIR": lahir,
        "USIA": usia,
        "TMT MASUK KERJA": tmt_masuk,
        "TMT PANGKAT": tmt_pangkat,
        "GOLONGAN": random.choice(golongan),
        "TMT PENSIUN": tmt_pensiun,
        "TAHUN PENSIUN": tmt_pensiun.year,
    }

# =========================================================
# 1. MASTER PEGAWAI: 200 AKTIF
# =========================================================
pegawai = [buat_pegawai(i) for i in range(1, 201)]
df_pegawai = pd.DataFrame(pegawai)

df_pegawai.to_excel(
    DATASET / "Data_Master.xlsx",
    index=False
)

df_pegawai.to_csv(
    DB / "employee" / "pegawai_kelola.csv",
    index=False,
    encoding="utf-8-sig"
)

# =========================================================
# 2. DATA ARSIP: 5 PEGAWAI FIKTIF TAMBAHAN
# =========================================================
arsip = []
for i in range(201, 206):
    row = buat_pegawai(i, arsip=True)
    row["STATUS ARSIP"] = "PENSIUN"
    row["TANGGAL ARSIP"] = date(2026, random.randint(1, 4), 15)
    row["KETERANGAN"] = "Pensiun"
    arsip.append(row)

pd.DataFrame(arsip).to_csv(
    DB / "employee" / "arsip_pegawai.csv",
    index=False,
    encoding="utf-8-sig"
)

# =========================================================
# 3. DATA KEHADIRAN: JANUARI-APRIL 2026
# =========================================================
kehadiran = []
tanggal = START

while tanggal <= END:
    # Hari kerja Senin-Jumat
    if tanggal.weekday() < 5:
        for p in pegawai:
            pilihan = random.choices(
                ["Hadir", "Izin", "Sakit", "Cuti", "Alpha"],
                weights=[93, 2, 2, 2, 1]
            )[0]

            terlambat = random.randint(1, 30) if pilihan == "Hadir" and random.random() < 0.12 else 0
            potongan = 100000 if pilihan == "Alpha" else 0

            kode = {
                "Hadir": "H",
                "Izin": "I",
                "Sakit": "S",
                "Cuti": "C",
                "Alpha": "A"
            }[pilihan]

            kehadiran.append({
                "nip": p["NIP BARU"],
                "nama": p["NAMA"],
                "opd": p["UNIT KERJA"],
                "tanggal": tanggal.isoformat(),
                "status_hadir": pilihan,
                "menit_terlambat": terlambat,
                "potong_gaji": potongan,
                "kode_asli": kode
            })

    tanggal += timedelta(days=1)

pd.DataFrame(kehadiran).to_csv(
    DB / "attendance" / "kehadiran_final.csv",
    index=False,
    encoding="utf-8-sig"
)

# =========================================================
# 4. KPI: JANUARI-APRIL 2026
# =========================================================
aspek = [
    "Orientasi_Pelayanan",
    "Akuntabel",
    "Kompeten",
    "Harmonis",
    "Loyal",
    "Adaptif",
    "Kolaboratif"
]

kpi = []

for bulan in range(1, 5):
    periode = f"2026-{bulan:02d}"

    for p in pegawai:
        nilai = {
            kolom: round(random.uniform(76, 98), 2)
            for kolom in aspek
        }

        rata = round(sum(nilai.values()) / len(aspek), 2)

        if rata < 75:
            kategori = "Dibawah Ekspektasi"
        elif rata <= 90:
            kategori = "Sesuai Ekspektasi"
        else:
            kategori = "Diatas Ekspektasi"

        kpi.append({
            "NIP": p["NIP BARU"],
            "NAMA": p["NAMA"],
            "Periode": periode,
            **nilai,
            "Rata_7_Aspek": rata,
            "Kategori_7_Aspek": kategori,
            "Waktu_Update": datetime(2026, bulan, 28, 10, 0, 0)
        })

pd.DataFrame(kpi).to_csv(
    DB / "performance" / "kpi_7aspek_final.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nSELESAI! DATA DEMO BERHASIL DIBUAT")
print(f"Pegawai aktif : {len(df_pegawai)}")
print(f"Pegawai arsip : {len(arsip)}")
print(f"Data kehadiran: {len(kehadiran)} baris")
print(f"Data KPI      : {len(kpi)} baris")
print(f"Periode       : Januari-April 2026")
print(f"Lokasi        : {BASE}")