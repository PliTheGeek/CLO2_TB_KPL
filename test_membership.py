import unittest
from unittest.mock import patch
from membership import handle_membership
from database import members_db

class TestMembership(unittest.TestCase):
    def setUp(self):
        members_db.clear()

    @patch('builtins.input', side_effect=[
        '1',              # Masuk menu REGISTER
        'B1234XYZ',       # Plat kendaraan
        'John Doe',       # Nama
        '4'               # Keluar menu membership
    ])
    def test_register_member(self, mock_input):
        handle_membership()
        self.assertIn('B1234XYZ', members_db)
        self.assertEqual(members_db['B1234XYZ']['status'], 'active')

    @patch('builtins.input', side_effect=[
        '1', 'B1234XYZ', 'John Doe',  # Daftar member
        '2', 'B1234XYZ',              # Cek status
        '4'                           # Exit
    ])
    def test_check_status(self, mock_input):
        handle_membership()
        self.assertEqual(members_db['B1234XYZ']['nama'], 'John Doe')

    @patch('builtins.input', side_effect=[
        '1', 'B1234XYZ', 'John Doe',  # Daftar member
        '3', 'B1234XYZ',              # Nonaktifkan
        '4'                           # Exit
    ])
    def test_deactivate_member(self, mock_input):
        handle_membership()
        self.assertEqual(members_db['B1234XYZ']['status'], 'inactive')

if __name__ == '__main__':
    unittest.main()
