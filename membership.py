from datetime import datetime
from database import members_db, config, membership_menu_table

def handle_membership():
    current_state = "MENU_MEMBERSHIP"
    while True:
        if current_state == "MENU_MEMBERSHIP":
            print("\n=== MENU MEMBERSHIP ===")
            
            # Menggunakan tabel untuk menampilkan menu membership
            for key, item in sorted(membership_menu_table.items()):
                print(f"{key}. {item['label']}")
                
            choice = input("Pilih menu: ")
            current_state = membership_menu_table.get(choice, {}).get("action", "MENU_MEMBERSHIP")

        elif current_state == "REGISTER":
            print("\n=== PENDAFTARAN MEMBERSHIP ===")
            plat = input("Masukkan plat kendaraan: ").upper()
            nama = input("Masukkan nama lengkap: ")
            
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

        elif current_state == "DEACTIVATE":
            print("\n=== NONAKTIFKAN MEMBERSHIP ===")
            plat = input("Masukkan plat kendaraan: ").upper()
            if plat in members_db:
                members_db[plat]["status"] = "inactive"
                print(f"Membership untuk plat {plat} telah dinonaktifkan.")
            else:
                print("Plat tidak terdaftar sebagai member.")
            current_state = "MENU_MEMBERSHIP"

        elif current_state == "EXIT":
            break