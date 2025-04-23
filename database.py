parkir = {
    "motor": [],
    "mobil": []
}

laporan = {
    "total_pendapatan": 0
}

config = {
    "tarif": {"motor": 3000, "mobil": 5000},
    "denda": {"motor": 20000, "mobil": 50000},
    "kapasitas": {"motor": 10, "mobil": 5},
    "denda_hilang": 500000,
    "denda_hilang_tidak_terdaftar": 1000000,
    "diskon_member": 0.25,  # 25% diskon untuk member
}

# Database membership baru
members_db = {}  # Format: {plat: {"nama": "John", "status": "active"}}