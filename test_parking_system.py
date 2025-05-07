#TESTING BY AHMAD JUNAIDI
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from database import parkir, laporan, config, members_db, main_menu_table
from main import main
from parking import tambah_kendaraan, keluar_parkir, status_slot_parkir
from membership import handle_membership

class TestParkingSystem(unittest.TestCase):
    def setUp(self):
        # Reset data sebelum setiap test
        parkir["motor"] = []
        parkir["mobil"] = []
        laporan["total_pendapatan"] = 0
        laporan["riwayat_transaksi"] = []
        members_db.clear()

    def test_1_main_menu_structure(self):
        print("\n=== TEST 1: Verifikasi Struktur Menu Utama ===")
        expected_menu = {
            "1": {"label": "Tambah Kendaraan", "action": "TAMBAH_KENDARAAN"},
            "2": {"label": "List Kendaraan", "action": "LIST_KENDARAAN"},
            "3": {"label": "Keluar Parkir", "action": "KELUAR_PARKIR"},
            "4": {"label": "Laporan Pendapatan", "action": "LAPORAN"},
            "5": {"label": "Membership", "action": "MEMBERSHIP"},
            "6": {"label": "Riwayat Transaksi", "action": "RIWAYAT"},
            "7": {"label": "Status Slot Parkir", "action": "STATUS_SLOT"},
            "8": {"label": "Exit", "action": "EXIT"}
        }
        self.assertDictEqual(main_menu_table, expected_menu)
        print("✓ Struktur menu utama sesuai dengan tabel yang didefinisikan")

    def test_2_add_vehicle(self):
        print("\n=== TEST 2: Tambah Kendaraan ===")
        with patch('builtins.input', side_effect=["motor", "Vario", "B1234AB"]):
            tambah_kendaraan()
        
        self.assertEqual(len(parkir["motor"]), 1)
        self.assertEqual(parkir["motor"][0]["merk"], "Vario")
        self.assertEqual(parkir["motor"][0]["plat"], "B1234AB")
        print("✓ Kendaraan motor berhasil ditambahkan")

    def test_3_parking_exit_normal(self):
        print("\n=== TEST 3: Keluar Parkir Normal ===")
        # Tambah kendaraan dulu
        parkir["motor"].append({
            "merk": "Vario",
            "plat": "B1234AB",
            "waktu_masuk": datetime.now() - timedelta(hours=1)
        })
        
        with patch('builtins.input', side_effect=["1", "motor", "Vario", "B1234AB"]):
            keluar_parkir()
        
        self.assertEqual(len(parkir["motor"]), 0)
        self.assertEqual(laporan["total_pendapatan"], 3000)
        print("✓ Kendaraan berhasil keluar dengan biaya normal")

    def test_4_parking_exit_lost_ticket(self):
        print("\n=== TEST 4: Keluar Parkir Karcis Hilang ===")
        parkir["mobil"].append({
            "merk": "Avanza",
            "plat": "B5678CD",
            "waktu_masuk": datetime.now() - timedelta(hours=2)
        })
        
        with patch('builtins.input', side_effect=["2", "mobil", "John Doe", "1990-01-01", "Jakarta", "Avanza", "B5678CD"]):
            keluar_parkir()
        
        self.assertEqual(len(parkir["mobil"]), 0)
        self.assertGreaterEqual(laporan["total_pendapatan"], 50000)  # Parkir + denda
        print("✓ Kendaraan berhasil keluar dengan denda karcis hilang")

    def test_5_membership_flow(self):
        print("\n=== TEST 5: Alur Membership ===")
        # Test pendaftaran member
        with patch('builtins.input', side_effect=["1", "B1234AB", "John Doe", "4"]):
            handle_membership()
        
        self.assertIn("B1234AB", members_db)
        self.assertEqual(members_db["B1234AB"]["nama"], "John Doe")
        print("✓ Pendaftaran member berhasil")
        
        # Test cek status member
        with patch('builtins.input', side_effect=["2", "B1234AB", "4"]):
            handle_membership()
        print("✓ Pengecekan status member berhasil")

    def test_6_parking_slots(self):
        print("\n=== TEST 6: Status Slot Parkir ===")
        parkir["motor"].append({"plat": "B1234AB"})
        
        with patch('builtins.print') as mock_print:
            status_slot_parkir()
            mock_print.assert_any_call("Motor: 1/10 (Sisa: 9)")
            mock_print.assert_any_call("Mobil: 0/5 (Sisa: 5)")
        print("✓ Status slot parkir menampilkan informasi yang benar")

if __name__ == '__main__':
    unittest.main(verbosity=2)