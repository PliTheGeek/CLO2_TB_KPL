parkir = {
    "motor": [],
    "mobil": []
}

laporan = {
    "total_pendapatan": 0,
    "riwayat_transaksi": []
}

# Tabel konfigurasi parkir
config = {
    "tarif": {"motor": 3000, "mobil": 5000},
    "denda": {"motor": 20000, "mobil": 50000},
    "kapasitas": {"motor": 10, "mobil": 5},
    "denda_hilang": 500000,
    "denda_hilang_tidak_terdaftar": 1000000,
    "diskon_member": 0.25,  # 25% diskon untuk member
}

# Database membership
members_db = {}  # Format: {plat: {"nama": "John", "status": "active"}}

# Tabel untuk menu utama
main_menu_table = {
    "1": {"label": "Tambah Kendaraan", "action": "TAMBAH_KENDARAAN"},
    "2": {"label": "List Kendaraan", "action": "LIST_KENDARAAN"},
    "3": {"label": "Keluar Parkir", "action": "KELUAR_PARKIR"},
    "4": {"label": "Laporan Pendapatan", "action": "LAPORAN"},
    "5": {"label": "Membership", "action": "MEMBERSHIP"},
    "6": {"label": "Riwayat Transaksi", "action": "RIWAYAT"},
    "7": {"label": "Status Slot Parkir", "action": "STATUS_SLOT"},
    "8": {"label": "Exit", "action": "EXIT"}
}

# Tabel untuk menu membership
membership_menu_table = {
    "1": {"label": "Daftar Membership", "action": "REGISTER"},
    "2": {"label": "Cek Status Membership", "action": "CHECK_STATUS"},
    "3": {"label": "Nonaktifkan Membership", "action": "DEACTIVATE"},
    "4": {"label": "Kembali ke Menu Utama", "action": "EXIT"}
}