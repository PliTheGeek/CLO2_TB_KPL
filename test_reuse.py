from menu import show_menu
from parking import tambah_kendaraan
from database import parkir

def test_show_menu():
    print("Testing Show Menu:")
    show_menu()
    print("Show Menu sukses dipanggil.\n")

def test_tambah_kendaraan_motor_dummy():
    print("Testing Tambah Kendaraan Dummy:")
    parkir["motor"].clear()  # Clear dulu biar bersih
    dummy_data = {
        "merk": "Honda",
        "plat": "B1234XYZ",
        "waktu_masuk": "Dummy"
    }
    parkir["motor"].append(dummy_data)
    print(parkir["motor"])
    print("Tambah kendaraan sukses.\n")

if __name__ == "__main__":
    test_show_menu()
    test_tambah_kendaraan_motor_dummy()
