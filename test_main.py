import unittest
from unittest.mock import patch

# Potongan logika state dari main.py yang mau kita uji  ,dimana ini merupakan code teknik table driven yang di testing
def get_next_state(pilihan):
    return {
        "1": "TAMBAH_KENDARAAN",
        "2": "LIST_KENDARAAN",
        "3": "KELUAR_PARKIR",
        "4": "LAPORAN",
        "5": "EXIT"
    }.get(pilihan, "MENU")

class TestMainMenuLogic(unittest.TestCase):
    def test_menu_option_1(self):
        self.assertEqual(get_next_state("1"), "TAMBAH_KENDARAAN")
        
    def test_menu_option_2(self):
        self.assertEqual(get_next_state("2"), "LIST_KENDARAAN")
    
    def test_menu_option_3(self):
        self.assertEqual(get_next_state("3"), "KELUAR_PARKIR")

    def test_menu_option_4(self):
        self.assertEqual(get_next_state("4"), "LAPORAN")
    
    def test_menu_option_5(self):
        self.assertEqual(get_next_state("5"), "EXIT")

    def test_menu_invalid_option(self):
        self.assertEqual(get_next_state("invalid"), "MENU")
        self.assertEqual(get_next_state(""), "MENU")
        self.assertEqual(get_next_state("9"), "MENU")

if __name__ == '__main__':
    unittest.main()
