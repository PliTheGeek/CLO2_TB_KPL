from datetime import datetime
from database import parkir, config, laporan, members_db

def tambah_kendaraan():
    motor_sisa = config["kapasitas"]["motor"] - len(parkir["motor"])
    mobil_sisa = config["kapasitas"]["mobil"] - len(parkir["mobil"])
    print(f"Sisa Slot - Motor: {motor_sisa}, Mobil: {mobil_sisa}")
    
    jenis = input("Masukkan jenis kendaraan (motor/mobil): ").lower()
    if jenis not in config["kapasitas"]:
        print("Jenis kendaraan tidak valid!")
        return
    
    if len(parkir[jenis]) >= config["kapasitas"][jenis]:
        print("Maaf, slot parkir penuh!")
        return
    
    merk = input("Masukkan merk kendaraan: ")
    plat = input("Masukkan nomor plat kendaraan: ")
    waktu_masuk = datetime.now()
    parkir[jenis].append({"merk": merk, "plat": plat, "waktu_masuk": waktu_masuk})
    print(f"Tiket parkir:\nMerk: {merk}\nPlat: {plat}\nWaktu Masuk: {waktu_masuk}")

def list_kendaraan():
    print("Daftar Kendaraan yang Sedang Parkir:")
    for jenis, kendaraan_list in parkir.items():
        print(f"\nJenis: {jenis.capitalize()}")
        for kendaraan in kendaraan_list:
            waktu_masuk = kendaraan["waktu_masuk"].strftime("%Y-%m-%d %H:%M:%S")
            print(f"Merk: {kendaraan['merk']}, Plat: {kendaraan['plat']}, Masuk: {waktu_masuk}")

def keluar_parkir():
    pilihan = input("Pilih metode keluar: 1. Karcis, 2. Karcis Hilang: ")
    jenis = input("Masukkan jenis kendaraan (motor/mobil): ").lower()
    
    if pilihan == "1":
        attempts = 0
        while attempts < 3:
            merk = input("Masukkan merk kendaraan: ")
            if any(k["merk"].lower() == merk.lower() for k in parkir.get(jenis, [])):
                break
            print("Merk kendaraan tidak ditemukan!")
            attempts += 1
        else:
            print("Gagal 3 kali, kembali ke menu utama.")
            return
        
        attempts = 0
        while attempts < 3:
            plat = input("Masukkan nomor plat kendaraan: ").upper()
            for kendaraan in parkir.get(jenis, []):
                if kendaraan["plat"] == plat and kendaraan["merk"].lower() == merk.lower():
                    waktu_masuk = kendaraan["waktu_masuk"]
                    lama_parkir = datetime.now() - waktu_masuk
                    jam = lama_parkir.total_seconds() // 3600
                    biaya = (jam // 2 + 1) * config["tarif"][jenis]
                    if plat in members_db and members_db[plat].get("status") == "active":
                        diskon = config.get("diskon_member", 0)
                        biaya_diskon = int(biaya * (1 - diskon))
                        print(f"\n=== INFO MEMBER ===")
                        print(f"Member aktif! Diskon: {diskon * 100}% diterapkan.")
                        print(f"Biaya normal: Rp{biaya}")
                        print(f"Biaya setelah diskon: Rp{biaya_diskon}")
                        biaya = biaya_diskon

                    laporan["total_pendapatan"] += biaya
                    parkir[jenis].remove(kendaraan)
                    print(f"Total biaya parkir: Rp{biaya}")
                    return
            print("Plat nomor tidak ditemukan!")
            attempts += 1
        print("Gagal 3 kali, kembali ke menu utama.")
        
    elif pilihan == "2":
        nama = input("Masukkan Nama Lengkap: ")
        tanggal_lahir = input("Masukkan Tanggal Lahir (YYYY-MM-DD): ")
        alamat = input("Masukkan Alamat: ")
        
        attempts = 0
        while attempts < 3:
            merk = input("Masukkan merk kendaraan: ")
            if any(k["merk"].lower() == merk.lower() for k in parkir.get(jenis, [])):
                break
            print("Merk kendaraan tidak ditemukan!")
            attempts += 1
        else:
            print("Plat Nomor Tidak Ditemukan!, denda Rp1.000.000 harus dibayar!")
            laporan["total_pendapatan"] += config["denda_hilang_tidak_terdaftar"]
            return
        
        attempts = 0
        while attempts < 3:
            plat = input("Masukkan nomor plat kendaraan: ").upper()
            for kendaraan in parkir.get(jenis, []):
                if kendaraan["plat"] == plat and kendaraan["merk"].lower() == merk.lower():
                    waktu_masuk = kendaraan["waktu_masuk"]
                    lama_parkir = datetime.now() - waktu_masuk
                    jam = lama_parkir.total_seconds() // 3600
                    biaya_parkir = (jam // 2 + 1) * config["tarif"][jenis]
                    biaya_denda = config["denda"][jenis]
                    biaya = biaya_parkir + biaya_denda
                    
                    # Pengecekan membership (hanya diskon untuk biaya parkir, bukan denda)
                    if plat in members_db and members_db[plat]["status"] == "active":
                        diskon = config["diskon_member"]
                        biaya_parkir_diskon = int(biaya_parkir * (1 - diskon))
                        biaya = biaya_parkir_diskon + biaya_denda
                        print(f"\n=== INFO MEMBER ===")
                        print(f"Member aktif! Diskon {diskon*100}% pada tarif parkir.")
                        print(f"Biaya parkir normal: Rp{biaya_parkir}")
                        print(f"Biaya parkir setelah diskon: Rp{biaya_parkir_diskon}")
                        print(f"Biaya denda tetap: Rp{biaya_denda}")
                    
                    laporan["total_pendapatan"] += biaya
                    parkir[jenis].remove(kendaraan)
                    print(f"\nTotal biaya parkir + denda: Rp{biaya}")
                    return
            print("Plat nomor tidak ditemukan!")
            attempts += 1
        print("Plat Nomor Tidak Ditemukan!, denda Rp1.000.000 harus dibayar!")
        laporan["total_pendapatan"] += config["denda_hilang_tidak_terdaftar"]
def force_keluar_parkir(plat_keluar):
    for jenis, daftar in parkir.items():
        for kendaraan in daftar:
            if kendaraan["plat"] == plat_keluar:
                daftar.remove(kendaraan)
                print(f"Kendaraan {plat_keluar} berhasil keluar dari parkiran (mode testing).")
                return
    print(f"Kendaraan dengan plat {plat_keluar} tidak ditemukan (mode testing).")
