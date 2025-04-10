from datetime import datetime
from database import parkir, config, laporan

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
            plat = input("Masukkan nomor plat kendaraan: ")
            for kendaraan in parkir.get(jenis, []):
                if kendaraan["plat"] == plat and kendaraan["merk"].lower() == merk.lower():
                    waktu_masuk = kendaraan["waktu_masuk"]
                    lama_parkir = datetime.now() - waktu_masuk
                    jam = lama_parkir.total_seconds() // 3600
                    biaya = (jam // 2 + 1) * config["tarif"][jenis]
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
            plat = input("Masukkan nomor plat kendaraan: ")
            for kendaraan in parkir.get(jenis, []):
                if kendaraan["plat"] == plat and kendaraan["merk"].lower() == merk.lower():
                    waktu_masuk = kendaraan["waktu_masuk"]
                    lama_parkir = datetime.now() - waktu_masuk
                    jam = lama_parkir.total_seconds() // 3600
                    biaya = (jam // 2 + 1) * config["tarif"][jenis] + config["denda"][jenis]
                    laporan["total_pendapatan"] += biaya
                    parkir[jenis].remove(kendaraan)
                    print(f"Total biaya parkir + denda: Rp{biaya}")
                    return
            print("Plat nomor tidak ditemukan!")
            attempts += 1
        print("Plat Nomor Tidak Ditemukan!, denda Rp1.000.000 harus dibayar!")
        laporan["total_pendapatan"] += config["denda_hilang_tidak_terdaftar"]
