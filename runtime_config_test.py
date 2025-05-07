# runtime_config_test.py

# Konfigurasi awal
config = {
    "tarif": {
        "motor": 3000,
        "mobil": 5000
    }
}

# Fungsi perhitungan biaya berdasarkan jenis kendaraan dan jam
def hitung_biaya(jenis_kendaraan, durasi_jam):
    return config['tarif'][jenis_kendaraan] * durasi_jam

# Fungsi uji
def test_runtime_configuration():
    print("=== TEST KONFIGURASI DEFAULT ===")
    biaya_awal = hitung_biaya("motor", 2)
    print(f"Tarif awal (2 jam): {biaya_awal}")
    assert biaya_awal == 6000, "Tarif awal salah"
    print("PASS: Tarif awal benar.")

    print("\n=== TEST KONFIGURASI RUNTIME ===")
    config['tarif']['motor'] = 4000  # Ubah saat runtime
    biaya_baru = hitung_biaya("motor", 2)
    print(f"Tarif setelah update (2 jam): {biaya_baru}")
    assert biaya_baru == 8000, "Tarif runtime salah"
    print("PASS: Tarif runtime berubah dan benar.")

# Jalankan uji jika file dijalankan langsung
if __name__ == "__main__":
    test_runtime_configuration()