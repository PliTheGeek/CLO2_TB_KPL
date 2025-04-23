from menu import show_menu
from parking import tambah_kendaraan, list_kendaraan, force_keluar_parkir
from database import parkir

def test_show_menu():
    print("Testing Show Menu (Test 4):")
    show_menu()
    print("Show Menu sukses dipanggil.\n")

def test_tambah_kendaraan_mobil_dummy():
    print("Testing Tambah Kendaraan Mobil Dummy (Test 4):")
    parkir["mobil"].clear()  # Clear data mobil dulu
    dummy_data = {
        "merk": "Toyota",
        "plat": "D7777YYY",
        "waktu_masuk": "Dummy"  # Dummy waktu
    }
    parkir["mobil"].append(dummy_data)
    print("Data setelah tambah dummy:")
    print(parkir["mobil"])
    print("Tambah kendaraan mobil sukses.\n")

def test_keluar_kendaraan_mobil_dummy():
    print("Testing Keluar Kendaraan Mobil Dummy (Test 4):")
    print("Sebelum keluar:", parkir["mobil"])
    plat_keluar = "D7777YYY"  # Plat dummy mobil
    force_keluar_parkir(plat_keluar)
    print("Sesudah keluar:", parkir["mobil"])
    print("Keluar kendaraan mobil sukses.\n")

if __name__ == "__main__":
    test_show_menu()
    test_tambah_kendaraan_mobil_dummy()
    test_keluar_kendaraan_mobil_dummy()
