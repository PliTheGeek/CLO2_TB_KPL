import os
from menu import show_menu
from parking import tambah_kendaraan, keluar_parkir, list_kendaraan
from report import laporan_pendapatan

def main():
    state = "MENU"
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        if state == "MENU":
            show_menu()
            pilihan = input("Pilih menu: ")
            
            state = {
                "1": "TAMBAH_KENDARAAN",
                "2": "LIST_KENDARAAN",
                "3": "KELUAR_PARKIR",
                "4": "LAPORAN",
                "5": "EXIT"
            }.get(pilihan, "MENU")
        
        if state == "TAMBAH_KENDARAAN":
            tambah_kendaraan()
            state = "MENU"
        elif state == "LIST_KENDARAAN":
            list_kendaraan()
            state = "MENU"
        elif state == "KELUAR_PARKIR":
            keluar_parkir()
            state = "MENU"
        elif state == "LAPORAN":
            laporan_pendapatan()
            state = "MENU"
        elif state == "EXIT":
            print("Terima kasih telah menggunakan layanan parkir!")
            break
        
        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()