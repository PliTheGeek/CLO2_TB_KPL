# membership.py
from datetime import datetime
from database import members_db, config

def handle_membership():
    current_state = "MENU_MEMBERSHIP"
    while True:
        if current_state == "MENU_MEMBERSHIP":
            print("\n=== MENU MEMBERSHIP ===")
            print("1. Daftar Membership")
            print("2. Cek Status Membership")
            print("3. Kembali ke Menu Utama")
            choice = input("Pilih menu: ")

            current_state = {
                "1": "REGISTER",
                "2": "CHECK_STATUS",
                "3": "EXIT"
            }.get(choice, "MENU_MEMBERSHIP")

        elif current_state == "REGISTER":
            print("\n=== PENDAFTARAN MEMBERSHIP ===")
            plat = input("Masukkan plat kendaraan: ").upper()
            nama = input("Masukkan nama lengkap: ")
            
            # Cek apakah plat sudah terdaftar
            if plat in members_db:
                print("Plat ini sudah terdaftar sebagai member!")
            else:
                members_db[plat] = {
                    "nama": nama,
                    "status": "active",
                    "tanggal_daftar": datetime.now().strftime("%Y-%m-%d")
                }
                print(f"Pendaftaran berhasil! Member untuk plat {plat} aktif.")
            current_state = "MENU_MEMBERSHIP"

        elif current_state == "CHECK_STATUS":
            print("\n=== CEK STATUS MEMBERSHIP ===")
            plat = input("Masukkan plat kendaraan: ").upper()
            member = members_db.get(plat)
            
            if member:
                print(f"\nStatus Member (Plat: {plat}):")
                print(f"Nama: {member['nama']}")
                print(f"Status: {member['status']}")
                print(f"Tanggal Daftar: {member['tanggal_daftar']}")
            else:
                print("Plat tidak terdaftar sebagai member.")
            current_state = "MENU_MEMBERSHIP"

        elif current_state == "EXIT":
            break