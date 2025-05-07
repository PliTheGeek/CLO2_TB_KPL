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

def status_slot_parkir():
    print("\n=== STATUS SLOT PARKIR ===")
    for jenis, kapasitas in config["kapasitas"].items():
        terisi = len(parkir[jenis])
        sisa = kapasitas - terisi
        print(f"{jenis.capitalize()}: {terisi}/{kapasitas} (Sisa: {sisa})")

def keluar_parkir():
    # Tabel metode keluar
    metode_keluar = {
        "1": {"label": "Karcis", "denda": False},
        "2": {"label": "Karcis Hilang", "denda": True}
    }
    
    print("\n=== METODE KELUAR ===")
    for key, item in sorted(metode_keluar.items()):
        print(f"{key}. {item['label']}")
    
    pilihan = input("Pilih metode keluar: ")
    metode = metode_keluar.get(pilihan)
    
    if not metode:
        print("Pilihan tidak valid!")
        return
    
    jenis = input("Masukkan jenis kendaraan (motor/mobil): ").lower()
    if jenis not in parkir:
        print("Jenis kendaraan tidak valid!")
        return
    
    # Proses keluar parkir dengan denda atau tanpa denda
    if metode["denda"]:
        print("\n=== PROSES KARCIS HILANG ===")
        nama = input("Masukkan Nama Lengkap: ")
        tanggal_lahir = input("Masukkan Tanggal Lahir (YYYY-MM-DD): ")
        alamat = input("Masukkan Alamat: ")
    
    attempts = 0
    while attempts < 3:
        merk = input("Masukkan merk kendaraan: ").strip().lower()
        plat = input("Masukkan nomor plat kendaraan: ").strip().upper()
        
        # Cari kendaraan yang sesuai
        kendaraan_ditemukan = None
        for kendaraan in parkir.get(jenis, []):
            if (kendaraan["merk"].lower() == merk and 
                kendaraan["plat"].upper() == plat):
                kendaraan_ditemukan = kendaraan
                break
        
        if kendaraan_ditemukan:
            waktu_masuk = kendaraan_ditemukan["waktu_masuk"]
            lama_parkir = datetime.now() - waktu_masuk
            jam = lama_parkir.total_seconds() // 3600
            biaya_parkir = (jam // 2 + 1) * config["tarif"][jenis]
            
            # Hitung biaya total
            if metode["denda"]:
                biaya_denda = config["denda"][jenis]
                biaya = biaya_parkir + biaya_denda
                keterangan = f"Parkir {jam} jam + Denda Karcis Hilang"
            else:
                biaya = biaya_parkir
                keterangan = f"Parkir {jam} jam"
            
            # Pengecekan membership
            if plat in members_db and members_db[plat].get("status") == "active":
                diskon = config["diskon_member"]
                biaya_parkir_diskon = int(biaya_parkir * (1 - diskon))
                biaya = biaya_parkir_diskon + (biaya_denda if metode["denda"] else 0)
                print(f"\n=== INFO MEMBER ===")
                print(f"Member aktif! Diskon {diskon*100}% pada tarif parkir.")
                print(f"Biaya parkir normal: Rp{biaya_parkir:,}")
                print(f"Biaya parkir setelah diskon: Rp{biaya_parkir_diskon:,}")
                if metode["denda"]:
                    print(f"Biaya denda tetap: Rp{biaya_denda:,}")
            
            laporan["total_pendapatan"] += biaya
            parkir[jenis].remove(kendaraan_ditemukan)
            
            # Catat transaksi
            laporan["riwayat_transaksi"].append({
                "jenis": jenis,
                "plat": plat,
                "jumlah": biaya,
                "keterangan": keterangan,
                "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "nama": nama if metode["denda"] else None,
                "metode": "Karcis Hilang" if metode["denda"] else "Normal"
            })
            
            print(f"\n=== RINCIAN BIAYA ===")
            print(f"Lama parkir: {jam} jam")
            if metode["denda"]:
                print(f"Biaya parkir: Rp{biaya_parkir:,}")
                print(f"Biaya denda: Rp{biaya_denda:,}")
            print(f"Total biaya: Rp{biaya:,}")
            return
        else:
            print("\nKendaraan Ditemukan!:")
            print(f"- Jenis kendaraan: {jenis}")
            print(f"- Merk kendaraan: {merk}")
            print(f"- Plat nomor: {plat}")
            print("  Terimkasih .")
            attempts += 1
    
    print("\nGagal 3 kali, kembali ke menu utama.")
    if metode["denda"]:
        print("Denda Rp1.000.000 harus dibayar karena kendaraan tidak terdaftar!")
        laporan["total_pendapatan"] += config["denda_hilang_tidak_terdaftar"]
        laporan["riwayat_transaksi"].append({
            "jenis": "denda",
            "plat": "Tidak Diketahui",
            "jumlah": config["denda_hilang_tidak_terdaftar"],
            "keterangan": "Denda kendaraan tidak terdaftar",
            "waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nama": nama,
            "metode": "Karcis Hilang"
        })

def force_keluar_parkir(plat_keluar):
    for jenis, daftar in parkir.items():
        for kendaraan in daftar:
            if kendaraan["plat"] == plat_keluar:
                daftar.remove(kendaraan)
                print(f"Kendaraan {plat_keluar} berhasil keluar dari parkiran (mode testing).")
                return
    print(f"Kendaraan dengan plat {plat_keluar} tidak ditemukan (mode testing).")