import __main__
import unittest
from pathlib import Path
from membership_system import (
    Member,
    determine_level,
    update_member_levels,
    save_members_to_csv,
    load_members_from_csv,
)


class TestDetermineLevel(unittest.TestCase):

    def test_gold_level(self):
        self.assertEqual(determine_level(10000), "Gold")
        self.assertEqual(determine_level(15000), "Gold")

    def test_silver_level(self):
        self.assertEqual(determine_level(5000), "Silver")
        self.assertEqual(determine_level(9999), "Silver")

    def test_bronze_level(self):
        self.assertEqual(determine_level(1000), "Bronze")
        self.assertEqual(determine_level(4999), "Bronze")

    def test_no_membership(self):
        self.assertEqual(determine_level(999), "No Membership")
        self.assertEqual(determine_level(0), "No Membership")

    def test_float_amount(self):
        self.assertEqual(determine_level(7500.75), "Silver")


class TestMember(unittest.TestCase):

    def test_full_name(self):
        m = Member("Test", "Name")
        self.assertEqual(m.full_name(), "Test Name")

    def test_default_values(self):
        m = Member("Test", "User")
        self.assertEqual(m.donation_level, "No Membership")
        self.assertEqual(m.total_donations, 0.0)

    def test_to_dict(self):
        m = Member("Alice", "Wonder", "Gold", 12000.0)
        d = m.to_dict()
        self.assertEqual(d["first_name"], "Alice")
        self.assertEqual(d["total_donations"], 12000.0)


class TestUpdateLevels(unittest.TestCase):

    def setUp(self):
        self.members = [
            Member("Frank", "Castle", "Bronze", 1200.0),
            Member("Gwen", "Stacy", "Silver", 6000.0),
            Member("Cindy", "Moon", "Gold", 15000.0),
        ]

    def test_level_upgrade(self):
        donation_data = {"Frank Castle": 9000}  # 1200 + 9000 = 10200 → Gold
        changed = update_member_levels(self.members, donation_data)
        self.assertTrue(changed)
        self.assertEqual(self.members[0].donation_level, "Gold")
        self.assertEqual(self.members[0].total_donations, 10200.0)

    def test_no_level_change(self):
        donation_data = {"Gwen Stacy": 1000}   # Still Silver
        changed = update_member_levels(self.members, donation_data)
        self.assertFalse(changed)
        self.assertEqual(self.members[1].donation_level, "Silver")

    def test_multiple_members_update(self):
        donation_data = {"Frank Castle": 4000, "Mike Mike": 2000}
        changed = update_member_levels(self.members, donation_data)
        self.assertTrue(changed)
        self.assertEqual(self.members[0].donation_level, "Silver")


class TestCSVOperations(unittest.TestCase):

    def setUp(self):
        self.test_file = "test_members_unittest.csv"
        self.members = [
            Member("Test1", "User", "Gold", 15000.0),
            Member("Test2", "User", "Bronze", 800.0),
        ]

    def tearDown(self):
        Path(self.test_file).unlink(missing_ok=True)

    def test_save_and_load_roundtrip(self):
        save_members_to_csv(self.members, self.test_file)
        loaded = load_members_from_csv(self.test_file)

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].full_name(), "Test1 User")
        self.assertEqual(loaded[0].donation_level, "Gold")
        self.assertEqual(loaded[0].total_donations, 15000.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)