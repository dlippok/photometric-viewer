import unittest

from photometric_viewer.utils.calc import annual_power_consumption, energy_cost, calculate_photometry, \
    required_number_of_luminaires
from tests.fixtures.photometry import *


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


class TestRquiredNumberOfLuminaires(unittest.TestCase):
    def test_energy_cost_with_correct_values(self):
        cases = [
            {
                "name": "Post-top luminaire on a small square",
                "flux_luminaire": 911,
                "mf": 0.8,
                "avg_illuminance": 10,
                "area": 250,
                "expected": 4
            },
            {
                "name": "Parking lot",
                "flux_luminaire": 10200,
                "mf": 0.8,
                "avg_illuminance": 10,
                "area": 2500,
                "expected": 4
            },
            {
                "name": "Office",
                "flux_luminaire": 3600,
                "mf": 0.8,
                "avg_illuminance": 500,
                "area": 60,
                "expected": 11
            },
            {
                "name": "Edge case: Minimum of 1 luminaire",
                "flux_luminaire": 10200,
                "mf": 0.8,
                "avg_illuminance": 10,
                "area": 0.25,
                "expected": 1
            },
        ]
        for case in cases:
            with(self.subTest(case["name"])):
                self.assertEqual(
                    required_number_of_luminaires(
                        fulx_luminaire=case["flux_luminaire"],
                        mf=case["mf"],
                        avg_illuminance=case["avg_illuminance"],
                        area=case["area"]
                    ),
                    case["expected"]
                )


class TestPhotometricProperties(unittest.TestCase):
    def test_calculates_values_correctly(self):
        """
        Test uniform radiating light sources
        """
        EXPECTED_FLUX = 1000 * 4 * math.pi
        cases = [
            {
                "title": "Equidistant uniform radiating source",
                "source": UNIFORM_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 0.5)
            },
            {
                "title": "Equidistant downward radiating source",
                "source": DOWNWARD_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 1)
            },
            {
                "title": "Equidistant upward radiating source",
                "source": UPWARD_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 0)
            },
            {
                "title": "Non equidistant uniform radiating source",
                "source": NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 0.5)
            },
            {
                "title": "Non equidistant downward radiating source",
                "source": NON_EQUIDISTANT_DOWNWARD_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 1)
            },
            {
                "title": "Non equidistant upward radiating source",
                "source": NON_EQUIDISTANT_UPWARD_RADIATING_SOURCE,
                "expected": (EXPECTED_FLUX, 1, 0)
            },
            {
                "title": "LOR 50 equidistant upward radiating source",
                "source": LOR_50_UNIFORM_RADIATING_SOURCE,
                "expected": (1000, 0.5, 0.5)
            }
        ]

        for case in cases:
            with(self.subTest(case=case, msg=case["title"])):
                properties = calculate_photometry(case["source"])
                self.assertAlmostEqual(properties.luminous_flux.value, case["expected"][0])
                self.assertAlmostEqual(properties.lor.value, case["expected"][1])
                self.assertAlmostEqual(properties.dff.value, case["expected"][2])

    def test_do_not_overwrite_existing_values(self):
        CALCULATED_FLUX = 1000 * 4 * math.pi
        CALCULATED_LOR = 1
        CALCULATED_DFF = 0.5
        WATTAGE = UNIFORM_RADIATING_SOURCE.lamps[0].wattage

        cases = [
            {
                "title": "All values are set",
                "source": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(0.8),
                    dff=Calculable(0.8),
                    efficacy=Calculable(999)
                ),
                "expected": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(0.8),
                    dff=Calculable(0.8),
                    efficacy=Calculable(999)
                )
            },
            {
                "title": "Calculated flux and efficacy",
                "source": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(None),
                    lor=Calculable(0.8),
                    dff=Calculable(0.8),
                    efficacy=Calculable(None)
                ),
                "expected": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(CALCULATED_FLUX, is_calculated=True),
                    lor=Calculable(0.8),
                    dff=Calculable(0.8),
                    efficacy=Calculable(CALCULATED_FLUX / WATTAGE, is_calculated=True)
                )
            },
            {
                "title": "Calculated LOR",
                "source": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(None),
                    dff=Calculable(0.8),
                    efficacy=Calculable(999)
                ),
                "expected": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(CALCULATED_LOR, is_calculated=True),
                    dff=Calculable(0.8),
                    efficacy=Calculable(999)
                )
            },
            {
                "title": "Calculated DFF",
                "source": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(0.8),
                    dff=Calculable(None),
                    efficacy=Calculable(999)
                ),
                "expected": LuminairePhotometricProperties(
                    is_absolute=True,
                    luminous_flux=Calculable(1000),
                    lor=Calculable(0.8),
                    dff=Calculable(CALCULATED_DFF, is_calculated=True),
                    efficacy=Calculable(999)
                )
            },

        ]
        for case in cases:
            with(self.subTest(case=case["title"])):
                luminaire = copy.deepcopy(UNIFORM_RADIATING_SOURCE)
                luminaire.photometry = case["source"]
                properties = calculate_photometry(luminaire)
                self.assertEqual(properties, case["expected"])