import unittest
from unittest.mock import patch
from parking import tambah_kendaraan, keluar_parkir, list_kendaraan, status_slot_parkir
from database import parkir, laporan, config

class TestParkir(unittest.TestCase):
    def setUp(self):
        # Reset parkir dan laporan sebelum setiap tes
        parkir["motor"].clear()
        parkir["mobil"].clear()
        laporan["total_pendapatan"] = 0
        laporan["riwayat_transaksi"].clear()

    @patch('builtins.input', side_effect=['motor', 'Honda', 'B1234XYZ'])
    def test_tambah_kendaraan_motor(self, mock_input):
        tambah_kendaraan()
        self.assertEqual(len(parkir["motor"]), 1)
        self.assertEqual(parkir["motor"][0]["plat"], 'B1234XYZ')

    @patch('builtins.input', side_effect=[
        'motor', 'Honda', 'B1234XYZ',  # tambah kendaraan
        '1', 'motor', 'honda', 'B1234XYZ'  # keluar parkir
    ])
    def test_keluar_kendaraan_normal(self, mock_input):
        tambah_kendaraan()
        keluar_parkir()
        self.assertEqual(len(parkir["motor"]), 0)
        self.assertGreaterEqual(laporan["total_pendapatan"], config["tarif"]["motor"])
        self.assertEqual(len(laporan["riwayat_transaksi"]), 1)

    def test_status_slot_parkir_output(self):
        with patch('builtins.print') as mock_print:
            status_slot_parkir()
            self.assertTrue(mock_print.called)

    def test_list_kendaraan_output(self):
        with patch('builtins.print') as mock_print:
            list_kendaraan()
            self.assertTrue(mock_print.called)

if __name__ == '__main__':
    unittest.main()
