from database import main_menu_table

def show_menu():
    print("=" * 40)
    print("     SISTEM PARKIR SEDERHANA")
    print("=" * 40)
    
    # Menggunakan tabel untuk menampilkan menu
    for key, item in sorted(main_menu_table.items()):
        print(f"{key}. {item['label']}")
    
    print("=" * 40)