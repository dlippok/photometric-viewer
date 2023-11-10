import json
import unittest

import photometric_viewer.formats.format_json
from photometric_viewer.model.photometry import LuminaireType
from tests.fixtures.photometry import ABSOLUTE_PHOTOMETRY_LUMINAIRE, TWO_LAMPS_LUMINAIRE, \
    LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY


class TestJson(unittest.TestCase):
    def test_geometry_with_luminaire(self):
        output = photometric_viewer.formats.format_json.export_photometry(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
        deserialized_output = json.loads(output)

        expected_geometry = {
                "luminaire": {
                    "shape": "RECTANGULAR",
                    "width": 0.4,
                    "length": 1.2,
                    "height": 0.15
                },
                "luminous_opening": {
                    "shape": "ROUND",
                    "width": 0.3,
                    "length": 0.5,
                    "height": 0.7,
                    "height_c90": 0.8,
                    "height_c180": 0.9,
                    "height_c270": 1.0
                }
        }
        self.assertEqual(deserialized_output["geometry"], expected_geometry)

    def test_geometry_without_luminaire(self):
        output = photometric_viewer.formats.format_json.export_photometry(LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY)
        deserialized_output = json.loads(output)

        expected_geometry = {
            "luminous_opening": {
                "shape": "ROUND",
                "width": 0.3,
                "length": 0.5,
                "height": 0.7,
                "height_c90": 0.8,
                "height_c180": 0.9,
                "height_c270": 1.0
            },
            "luminaire": None
        }
        self.assertEqual(deserialized_output["geometry"], expected_geometry)

    def test_photometry(self):
        output = photometric_viewer.formats.format_json.export_photometry(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
        deserialized_output = json.loads(output)

        expected_photometry = {
            "is_absolute": True,
            "gamma_angles": [0, 45, 90],
            "c_planes": [0, 90, 180, 270],
            "values": [
                {'c': 0, 'gamma': 0, 'value': 300},
                {'c': 0, 'gamma': 45, 'value': 100},
                {'c': 0, 'gamma': 90, 'value': 20},
                {'c': 90, 'gamma': 0, 'value': 300},
                {'c': 90, 'gamma': 45, 'value': 100},
                {'c': 90, 'gamma': 90, 'value': 20},
                {'c': 180, 'gamma': 0, 'value': 300},
                {'c': 180, 'gamma': 45, 'value': 100},
                {'c': 180, 'gamma': 90, 'value': 20},
                {'c': 270, 'gamma': 0, 'value': 300},
                {'c': 270, 'gamma': 45, 'value': 100},
                {'c': 270, 'gamma': 90, 'value': 20},
            ],
            "dff": 100,
            "lorl": 100
        }
        self.assertEqual(deserialized_output["photometry"], expected_photometry)

    def test_single_lamp(self):
        output = photometric_viewer.formats.format_json.export_photometry(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
        deserialized_output = json.loads(output)

        expected_lamps = [
            {
                "number_of_lamps": 1,
                "description": "Test lamp",
                "catalog_number": "LP1220",
                "position": "center",
                "lumens_per_lamp": 1200,
                "wattage": 80,
                "color": "6000K",
                "cri": "95",
                "ballast_description": "Test Ballast",
                "ballast_catalog_number": "BL2500"
            }
        ]
        self.assertEqual(deserialized_output["lamp_sets"], expected_lamps)

    def test_multiple_lamps(self):
        output = photometric_viewer.formats.format_json.export_photometry(TWO_LAMPS_LUMINAIRE)
        deserialized_output = json.loads(output)

        expected_lamps = [
            {
                "number_of_lamps": 1,
                "description": "Test lamp 1",
                "catalog_number": "LP1221",
                "position": "center",
                "lumens_per_lamp": 1200,
                "wattage": 80,
                "color": "6000K",
                "cri": "95",
                "ballast_description": "Test Ballast",
                "ballast_catalog_number": "BL2501"
            },
            {
                "number_of_lamps": 2,
                "description": "Test lamp 2",
                "catalog_number": "LP1222",
                "position": "center",
                "lumens_per_lamp": 1100,
                "wattage": 75,
                "color": "6500K",
                "cri": "90",
                "ballast_description": "Test Ballast 2",
                "ballast_catalog_number": "BL2502"
            }

        ]
        self.assertEqual(deserialized_output["lamp_sets"], expected_lamps)

    def test_metadata(self):
        photometry = ABSOLUTE_PHOTOMETRY_LUMINAIRE
        output = photometric_viewer.formats.format_json.export_photometry(photometry)
        deserialized_output = json.loads(output)

        expected_metadata = {
            "luminaire": "Test Luminaire",
            "catalog_number": "LM600",
            "manufacturer": "Test",
            "luminaire_type": LuminaireType.LINEAR.name,
            "measurement": "MS123",
            "date_and_user": "2023-07-09",
            "additional_properties": {
                "ADDITIONAL": "PROPERTY"
            }
        }
        self.assertEqual(deserialized_output["metadata"], expected_metadata)
