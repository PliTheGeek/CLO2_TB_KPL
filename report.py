from database import laporan

def laporan_pendapatan():
    print(f"Total Pendapatan Parkir: Rp{laporan['total_pendapatan']}")