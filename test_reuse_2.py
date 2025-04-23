from menu import show_menu
from parking import tambah_kendaraan, list_kendaraan, force_keluar_parkir
from database import parkir

def test_show_menu():
    print("Testing Show Menu (Test 3):")
    show_menu()
    print("Show Menu sukses dipanggil.\n")

def test_tambah_kendaraan_motor_dummy():
    print("Testing Tambah Kendaraan Dummy (Test 3):")
    parkir["motor"].clear() 
    dummy_data = {
        "merk": "Yamaha",
        "plat": "E9999ZZZ",
        "waktu_masuk": "Dummy" 
    }
    parkir["motor"].append(dummy_data)
    print("Data setelah tambah dummy:")
    print(parkir["motor"])
    print("Tambah kendaraan sukses.\n")

def test_keluar_kendaraan_dummy():
    print("Testing Keluar Kendaraan Dummy (Test 3):")
    print("Sebelum keluar:", parkir["motor"])
    plat_keluar = "E9999ZZZ"
    force_keluar_parkir(plat_keluar)
    print("Sesudah keluar:", parkir["motor"])
    print("Keluar kendaraan sukses.\n")

if __name__ == "__main__":
    test_show_menu()
    test_tambah_kendaraan_motor_dummy()
    test_keluar_kendaraan_dummy()