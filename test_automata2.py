import unittest
import io
from contextlib import redirect_stdout
from unittest.mock import patch  # Import modul mock
from membership import handle_membership
from database import members_db

def get_next_membership_state(current_state, input_symbol):
    transition_table = {
        "MENU_MEMBERSHIP": {
            "1": "REGISTER",
            "2": "CHECK_STATUS",
            "3": "EXIT"
        },
        "REGISTER": {"": "MENU_MEMBERSHIP"},
        "CHECK_STATUS": {"": "MENU_MEMBERSHIP"},
        "EXIT": {"": "EXIT"}
    }
    return transition_table.get(current_state, {}).get(input_symbol, "MENU_MEMBERSHIP")

class TestMembershipAutomata(unittest.TestCase):
    def setUp(self):
        members_db.clear()
        members_db["B1234X"] = {
            "nama": "John Doe",
            "status": "active",
            "tanggal_daftar": "2023-01-01"
        }

    def test_valid_transitions_from_menu(self):
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "1"), "REGISTER")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "2"), "CHECK_STATUS")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "3"), "EXIT")

    def test_invalid_input_from_menu(self):
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "x"), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", ""), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("MENU_MEMBERSHIP", "9"), "MENU_MEMBERSHIP")

    def test_back_to_menu_after_actions(self):
        self.assertEqual(get_next_membership_state("REGISTER", ""), "MENU_MEMBERSHIP")
        self.assertEqual(get_next_membership_state("CHECK_STATUS", ""), "MENU_MEMBERSHIP")

    def test_exit_state_stays(self):
        self.assertEqual(get_next_membership_state("EXIT", ""), "EXIT")

    def test_check_status_output(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            with patch('builtins.input', side_effect=['2', 'B1234X', '3']):  # Input sequence
                handle_membership()
            output = buf.getvalue()
        
        self.assertIn("Status: active", output)
        self.assertIn("Nama: John Doe", output)
        self.assertIn("Tanggal Daftar: 2023-01-01", output)

if __name__ == '__main__':
    unittest.main()