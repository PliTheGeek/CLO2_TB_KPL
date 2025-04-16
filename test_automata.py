import unittest

def get_next_state(current_state, input_symbol):
    transition_table = {
        "MENU": {
            "1": "TAMBAH_KENDARAAN",
            "2": "LIST_KENDARAAN",
            "3": "KELUAR_PARKIR",
            "4": "LAPORAN",
            "5": "EXIT"
        },
        "TAMBAH_KENDARAAN": {"": "MENU"},
        "LIST_KENDARAAN": {"": "MENU"},
        "KELUAR_PARKIR": {"": "MENU"},
        "LAPORAN": {"": "MENU"},
        "EXIT": {"": "EXIT"},
    }
    return transition_table.get(current_state, {}).get(input_symbol, current_state)

class TestAutomata(unittest.TestCase):
    def test_valid_transitions_from_menu(self):
        self.assertEqual(get_next_state("MENU", "1"), "TAMBAH_KENDARAAN")
        self.assertEqual(get_next_state("MENU", "2"), "LIST_KENDARAAN")
        self.assertEqual(get_next_state("MENU", "3"), "KELUAR_PARKIR")
        self.assertEqual(get_next_state("MENU", "4"), "LAPORAN")
        self.assertEqual(get_next_state("MENU", "5"), "EXIT")

    def test_invalid_input_from_menu(self):
        self.assertEqual(get_next_state("MENU", "x"), "MENU")
        self.assertEqual(get_next_state("MENU", ""), "MENU")
        self.assertEqual(get_next_state("MENU", "9"), "MENU")

    def test_back_to_menu_after_actions(self):
        self.assertEqual(get_next_state("TAMBAH_KENDARAAN", ""), "MENU")
        self.assertEqual(get_next_state("LIST_KENDARAAN", ""), "MENU")
        self.assertEqual(get_next_state("KELUAR_PARKIR", ""), "MENU")
        self.assertEqual(get_next_state("LAPORAN", ""), "MENU")

    def test_exit_state_stays(self):
        self.assertEqual(get_next_state("EXIT", ""), "EXIT")

if __name__ == '__main__':
    unittest.main()
