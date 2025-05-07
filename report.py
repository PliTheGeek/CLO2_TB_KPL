from database import laporan

def laporan_pendapatan():
    print(f"\n=== LAPORAN PENDAPATAN ===")
    print(f"Total Pendapatan Parkir: Rp{laporan['total_pendapatan']:,}")

def riwayat_transaksi():
    print("\n=== RIWAYAT TRANSAKSI ===")
    if not laporan["riwayat_transaksi"]:
        print("Belum ada transaksi.")
        return
    
    for transaksi in laporan["riwayat_transaksi"]:
        print(f"\nWaktu: {transaksi['waktu']}")
        print(f"Plat: {transaksi.get('plat', '-')}")
        print(f"Jenis: {transaksi.get('jenis', '-')}")
        print(f"Keterangan: {transaksi.get('keterangan', '-')}")
        print(f"Jumlah: Rp{transaksi['jumlah']:,}")