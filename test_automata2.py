import unittest
import io
from contextlib import redirect_stdout
from unittest.mock import patch
from membership import handle_membership
from database import members_db

def get_next_membership_state(current_state, input_symbol):
    """Fungsi bantu untuk menentukan state berikutnya"""
    transition_table = {
        "MENU_MEMBERSHIP": {
            "1": "REGISTER",
            "2": "CHECK_STATUS",
            "3": "DEACTIVATE",
            "4": "EXIT"
        },
        "REGISTER": {"": "MENU_MEMBERSHIP"},
        "CHECK_STATUS": {"": "MENU_MEMBERSHIP"},
        "DEACTIVATE": {"": "MENU_MEMBERSHIP"},
        "EXIT": {"": "EXIT"}
    }
    return transition_table.get(current_state, {}).get(input_symbol, "MENU_MEMBERSHIP")

class TestMembershipAutomata(unittest.TestCase):
    def setUp(self):
        """Setup data testing sebelum setiap test dijalankan"""
        members_db.clear()
        members_db["B1234X"] = {
            "nama": "John Doe",
            "status": "active",
            "tanggal_daftar": "2023-01-01"
        }

    def test_valid_transitions_from_menu(self):
        """Test transisi valid dari menu utama"""
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "1"), "REGISTER")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "2"), "CHECK_STATUS")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "3"), "DEACTIVATE")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "4"), "EXIT")

    def test_invalid_input_from_menu(self):
        """Test input tidak valid dari menu utama"""
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "x"), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", ""), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "9"), "MENU_MEMBERSHIP")

    def test_back_to_menu_after_actions(self):
        """Test kembali ke menu setelah aksi selesai"""
        self.assertEqual(get_next_membership_state("REGISTER", ""), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("CHECK_STATUS", ""), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("DEACTIVATE", ""), "MENU_MEMBERSHIP")

    def test_exit_state_stays(self):
        """Test state exit tetap stabil"""
        self.assertEqual(get_next_membership_state("EXIT", ""), "EXIT")

    def test_check_status_output(self):
        """Test output pengecekan status membership"""
        with io.StringIO() as buf, redirect_stdout(buf):
            # Sequence input: 
            # 2 -> menu cek status
            # B1234X -> input plat
            # '' -> kembali ke menu
            # 4 -> exit
            with patch('builtins.input', side_effect=['2', 'B1234X', '', '4']):
                handle_membership()
            output = buf.getvalue()
        
        # Verifikasi output mengandung informasi yang diharapkan
        self.assertIn("=== CEK STATUS MEMBERSHIP ===", output)
        self.assertIn("Status Member (Plat: B1234X):", output)
        self.assertIn("Nama: John Doe", output)
        self.assertIn("Status: active", output)
        self.assertIn("Tanggal Daftar: 2023-01-01", output)

    def test_register_new_member(self):
        """Test pendaftaran member baru"""
        with io.StringIO() as buf, redirect_stdout(buf):
            # Sequence input:
            # 1 -> menu registrasi
            # B5678Y -> plat baru
            # Jane Doe -> nama member
            # '' -> kembali ke menu
            # 4 -> exit
            with patch('builtins.input', side_effect=['1', 'B5678Y', 'Jane Doe', '', '4']):
                handle_membership()
            output = buf.getvalue()
        
        # Verifikasi output dan data
        self.assertIn("Pendaftaran berhasil! Member untuk plat B5678Y aktif.", output)
        self.assertIn("B5678Y", members_db)
        self.assertEqual(members_db["B5678Y"]["nama"], "Jane Doe")
        self.assertEqual(members_db["B5678Y"]["status"], "active")

    def test_deactivate_member(self):
        """Test menonaktifkan membership"""
        with io.StringIO() as buf, redirect_stdout(buf):
            # Sequence input:
            # 3 -> menu deaktivasi
            # B1234X -> plat member
            # '' -> kembali ke menu
            # 4 -> exit
            with patch('builtins.input', side_effect=['3', 'B1234X', '', '4']):
                handle_membership()
            output = buf.getvalue()
        
        # Verifikasi output dan data
        self.assertIn("Membership untuk plat B1234X telah dinonaktifkan.", output)
        self.assertEqual(members_db["B1234X"]["status"], "inactive")

if __name__ == '__main__':
    unittest.main()