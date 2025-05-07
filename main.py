import os
from menu import show_menu
from parking import tambah_kendaraan, keluar_parkir, list_kendaraan, status_slot_parkir
from report import laporan_pendapatan, riwayat_transaksi
from membership import handle_membership
from database import main_menu_table

def main():
    state = "MENU"
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        
        if state == "MENU":
            show_menu()
            pilihan = input("Pilih menu: ")
            
            # Menggunakan tabel untuk menentukan state berikutnya
            state = main_menu_table.get(pilihan, {}).get("action", "MENU")
        
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
        elif state == "MEMBERSHIP":
            handle_membership()
            state = "MENU"
        elif state == "RIWAYAT":
            riwayat_transaksi()
            state = "MENU"
        elif state == "STATUS_SLOT":
            status_slot_parkir()
            state = "MENU"
        elif state == "EXIT":
            print("Terima kasih telah menggunakan layanan parkir!")
            break
        
        input("Tekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()