import unittest

from photometric_viewer.utils.calc import annual_power_consumption, energy_cost


class TestPowerConsumption(unittest.TestCase):
    def test_power_consumption_with_correct_values(self):
        cases = [
            {"wattage": 100, "hours_per_day": 2.5, "expected_consumption": 100/1000 * 2.5 * 365},
            {"wattage": 0.5, "hours_per_day": 24, "expected_consumption": 0.5/1000 * 24 * 365},
            {"wattage": 0, "hours_per_day": 12, "expected_consumption": 0},
            {"wattage": 50, "hours_per_day": 0, "expected_consumption": 0},
            {"wattage": 0, "hours_per_day": 0, "expected_consumption": 0}
        ]
        for case in cases:
            with(self.subTest(case=case)):
                self.assertEqual(
                    annual_power_consumption(wattage=case["wattage"], daily_hours=case["hours_per_day"]),
                    case["expected_consumption"]
                )

    def test_power_consumption_with_negative_power(self):
        with self.assertRaises(ValueError):
            annual_power_consumption(wattage=-1, daily_hours=6)

    def test_power_consumption_with_negative_hours(self):
        with self.assertRaises(ValueError):
            annual_power_consumption(wattage=1, daily_hours=-1)

    def test_power_consumption_with_more_than_24_hours(self):
        with self.assertRaises(ValueError):
            annual_power_consumption(wattage=1, daily_hours=24.1)


class TestEnergyCost(unittest.TestCase):
    def test_energy_cost_with_correct_values(self):
        cases = [
            {"consumption_kwh": 1, "price_kwh": 0.25, "expected_cost": 0.25},
            {"consumption_kwh": 2, "price_kwh": 0.25, "expected_cost": 0.50},
            {"consumption_kwh": 100, "price_kwh": 0.25, "expected_cost": 25},
            {"consumption_kwh": 0, "price_kwh": 0.25, "expected_cost": 0},
            {"consumption_kwh": 100, "price_kwh": 0, "expected_cost": 0},
        ]
        for case in cases:
            with(self.subTest(case=case)):
                self.assertEqual(
                    energy_cost(power_consumption_kwh=case["consumption_kwh"], price_kwh=case["price_kwh"]),
                    case["expected_cost"]
                )

    def test_energy_cost_with_negative_consumption(self):
        with self.assertRaises(ValueError):
            energy_cost(power_consumption_kwh=-1, price_kwh=0.25)

    def test_energy_cost_with_negative_price(self):
        with self.assertRaises(ValueError):
            energy_cost(power_consumption_kwh=1, price_kwh=-0.25)