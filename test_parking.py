import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from database import parkir, laporan, config, members_db
from parking import keluar_parkir

class TestKeluarParkir(unittest.TestCase):
    def setUp(self):
        parkir["motor"].clear()
        parkir["mobil"].clear()
        laporan["total_pendapatan"] = 0
        laporan["riwayat_transaksi"].clear()
        members_db.clear()

        # Tambahkan kendaraan motor ke parkir
        waktu_masuk = datetime.now() - timedelta(hours=2)  # parkir 2 jam
        parkir["motor"].append({
            "merk": "Yamaha",
            "plat": "B1234XYZ",
            "waktu_masuk": waktu_masuk
        })

    @patch('builtins.input', side_effect=[
        '1',              # Pilih metode karcis normal
        'motor',          # Jenis kendaraan
        'yamaha',         # Merk kendaraan
        'B1234XYZ'        # Plat kendaraan
    ])
    def test_keluar_normal(self, mock_input):
        keluar_parkir()
        self.assertEqual(len(parkir["motor"]), 0)
        self.assertEqual(len(laporan["riwayat_transaksi"]), 1)
        self.assertGreaterEqual(laporan["total_pendapatan"], config["tarif"]["motor"])

    @patch('builtins.input', side_effect=[
        '2',                  # Pilih metode karcis hilang
        'motor',              # Jenis kendaraan
        'John Doe',           # Nama
        '1999-01-01',         # Tanggal lahir
        'Jl. Mawar No.1',     # Alamat
        'yamaha',             # Merk kendaraan
        'B1234XYZ'            # Plat kendaraan
    ])
    def test_keluar_denda(self, mock_input):
        keluar_parkir()
        self.assertEqual(len(parkir["motor"]), 0)
        self.assertEqual(len(laporan["riwayat_transaksi"]), 1)
        self.assertIn("Denda", laporan["riwayat_transaksi"][0]["keterangan"])
        self.assertGreaterEqual(laporan["total_pendapatan"], config["denda"]["motor"])

    @patch('builtins.input', side_effect=[
        '1', 'motor', 'salah', 'SALAH',  # 1st fail
        'salah', 'SALAH',                # 2nd fail
        'salah', 'SALAH'                 # 3rd fail
    ])
    def test_gagal_keluar_3_kali(self, mock_input):
        keluar_parkir()
        self.assertEqual(len(parkir["motor"]), 1)  # kendaraan tetap ada

if __name__ == '__main__':
    unittest.main()
