import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape, LuminaireGeometry, Shape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ldt.converter import convert_content
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


class TestConvertContent(unittest.TestCase):
    def test_empty_content(self):
        content = LdtContent(
            header="Manufacturer",
            type_indicator=1,
            symmetry_indicator=1,
            number_of_c_planes=1,
            distance_between_c_planes=0,
            number_of_intensities=37,
            distance_between_intensities=2.5,
            measurement_report="MEAS1",
            luminaire_name="Luminaire 1",
            luminaire_number="Lum1",
            file_name="Lum1.ldt",
            date_and_user="2024-03-10 Test User",
            length_of_luminaire=1000,
            width_of_luminaire=500,
            height_of_luminaire=300,
            length_of_luminous_area=1000,
            width_of_luminous_area=500,
            height_of_luminous_area_c0=300,
            height_of_luminous_area_c90=300,
            height_of_luminous_area_c180=300,
            height_of_luminous_area_c270=300,
            dff_percent=100,
            lor_percent=100,
            conversion_factor=1.0,
            tilt=0,
            number_of_lamp_sets=1,
            lamp_sets=[
                LampSet(
                    number_of_lamps=1,
                    type_of_lamp="Lamp 1",
                    total_lumens=1000,
                    light_color="White",
                    cri="80",
                    wattage=100
                )
            ],
            direct_ratios_for_room_indices=[
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
            ],
            c_angles=[0],
            gamma_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0,
                27.5, 30.0, 32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0,
                52.5, 55.0, 57.5, 60.0, 62.5, 65.0, 67.5, 70.0, 72.5, 75.0,
                77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4,
                600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5, 320.0, 185.0,
                100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0, 10.8, 10.8, 10.0,
                7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
            ]
        )

        expected = Luminaire(
            luminous_opening_geometry=case["expected"],
            geometry=None,
            lamps=[],
            metadata=PhotometryMetadata(
                catalog_number=None,
                luminaire=None,
                manufacturer=None,
                date_and_user=None,
                file_source=None,
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=False,
                luminous_flux=Calculable(None),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(None)
            ),
            gamma_angles = [],
            c_planes = [],
            intensity_values = {},
        )

        self.assertEqual(convert_content(content), expected)

    def test_full_absolute_photometry(self):


    def test_luminous_opening_geometry(self):
        test_cases = [
            {
                "title": "Point",
                "dimensions": (0, 0, 0, 0, 0, 0),
                "expected": LuminousOpeningGeometry(
                    length=0,
                    width=0,
                    height=0,
                    height_c90=0,
                    height_c180=0,
                    height_c270=0,
                    shape=LuminousOpeningShape.POINT
                )
            },
            {
                "title": "Rectangular",
                "dimensions": (100, 200, 300, 400, 500, 600),
                "expected": LuminousOpeningGeometry(
                    length=0.1,
                    width=0.2,
                    height=0.3,
                    height_c90=0.4,
                    height_c180=0.5,
                    height_c270=0.6,
                    shape=LuminousOpeningShape.RECTANGULAR
                )
            },
            {

                "title": "Round",
                "dimensions": (100, 0, 300, 400, 500, 600),
                "expected": LuminousOpeningGeometry(
                    length=0.1,
                    width=0.1,
                    height=0.3,
                    height_c90=0.4,
                    height_c180=0.5,
                    height_c270=0.6,
                    shape=LuminousOpeningShape.ROUND
                )
            },
            {
                "title": "Rectangular with zero heights",
                "dimensions": (100, 200, 0, 0, 0, 0),
                "expected": LuminousOpeningGeometry(
                    length=0.1,
                    width=0.2,
                    height=0,
                    height_c90=0,
                    height_c180=0,
                    height_c270=0,
                    shape=LuminousOpeningShape.RECTANGULAR
                )
            },
            {
                "title": "Round with zero heights",
                "dimensions": (100, 0, 0, 0, 0, 0),
                "expected": LuminousOpeningGeometry(
                    length=0.1,
                    width=0.1,
                    height=0,
                    height_c90=0,
                    height_c180=0,
                    height_c270=0,
                    shape=LuminousOpeningShape.ROUND
                )
            },
            {
                "title": "None length",
                "dimensions": (None, 200, 300, 400, 500, 600),
                "expected": None
            },
            {
                "title": "None width",
                "dimensions": (100, None, 300, 400, 500, 600),
                "expected": None
            },
            {
                "title": "None height c0",
                "dimensions": (100, 200, None, 400, 500, 600),
                "expected": None
            },
            {
                "title": "None height c90",
                "dimensions": (100, 200, 300, None, 500, 600),
                "expected": None
            },
            {
                "title": "None height c180",
                "dimensions": (100, 200, 300, 400, None, 600),
                "expected": None
            },
            {
                "title": "None height c270",
                "dimensions": (100, 200, 300, 400, 500, None),
                "expected": None
            },
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = LdtContent(
                    length_of_luminous_area=case["dimensions"][0],
                    width_of_luminous_area=case["dimensions"][1],
                    height_of_luminous_area_c0=case["dimensions"][2],
                    height_of_luminous_area_c90=case["dimensions"][3],
                    height_of_luminous_area_c180=case["dimensions"][4],
                    height_of_luminous_area_c270=case["dimensions"][5]
                )

                expected = Luminaire(
                    gamma_angles=[],
                    c_planes=[],
                    intensity_values={},
                    luminous_opening_geometry=case["expected"],
                    geometry=None,
                    lamps=[],
                    metadata=PhotometryMetadata(
                        catalog_number=None,
                        luminaire=None,
                        manufacturer=None,
                        date_and_user=None,
                        file_source=None,
                        file_format=FileFormat.LDT,
                        file_units=LengthUnits.MILLIMETERS
                    ),
                    photometry=LuminairePhotometricProperties(
                        is_absolute=False,
                        luminous_flux=Calculable(None),
                        lor=Calculable(None),
                        dff=Calculable(None),
                        efficacy=Calculable(None)
                    )
                )

                self.assertEqual(convert_content(content), expected)

    def test_luminaire_geometry(self):
        test_cases = [
            {
                "title": "Rectangular",
                "dimensions": (100, 200, 300),
                "expected": LuminaireGeometry(length=0.1, width=0.2, height=0.3, shape=Shape.RECTANGULAR)
            },
            {
                "title": "Round",
                "dimensions": (100, 0, 300),
                "expected": LuminaireGeometry(length=0.1, width=0.1, height=0.3, shape=Shape.ROUND)
            },
            {
                "title": "Rectangular zero height",
                "dimensions": (100, 200, 0),
                "expected": LuminaireGeometry(length=0.1, width=0.2, height=0, shape=Shape.RECTANGULAR)
            },
            {
                "title": "Round zero height",
                "dimensions": (100, 0, 0),
                "expected": LuminaireGeometry(length=0.1, width=0.1, height=0, shape=Shape.ROUND)
            },
            {
                "title": "Missing Length",
                "dimensions": (None, 200, 300),
                "expected": None
            },
            {
                "title": "Missing Width",
                "dimensions": (100, None, 300),
                "expected": None
            },
            {
                "title": "Missing Height",
                "dimensions": (100, 200, None),
                "expected": None
            },
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = LdtContent(
                    length_of_luminaire=case["dimensions"][0],
                    width_of_luminaire=case["dimensions"][1],
                    height_of_luminaire=case["dimensions"][2]
                )

                expected = Luminaire(
                    gamma_angles=[],
                    c_planes=[],
                    intensity_values={},
                    luminous_opening_geometry=None,
                    geometry=case["expected"],
                    lamps=[],
                    metadata=PhotometryMetadata(
                        catalog_number=None,
                        luminaire=None,
                        manufacturer=None,
                        date_and_user=None,
                        file_source=None,
                        file_format=FileFormat.LDT,
                        file_units=LengthUnits.MILLIMETERS
                    ),
                    photometry=LuminairePhotometricProperties(
                        is_absolute=False,
                        luminous_flux=Calculable(None),
                        lor=Calculable(None),
                        dff=Calculable(None),
                        efficacy=Calculable(None)
                    )
                )

                self.assertEqual(convert_content(content), expected)

    def test_multiple_lamp_sets(self):
        content = LdtContent(
            number_of_lamp_sets=2,
            lamp_sets=[
                LampSet(
                    number_of_lamps=1,
                    type_of_lamp="Lamp 1",
                    total_lumens=1000,
                    light_color="White",
                    cri="80",
                    wattage=100
                ),
                LampSet(
                    number_of_lamps=2,
                    type_of_lamp="Lamp 2",
                    total_lumens=1400,
                    light_color="Warm White",
                    cri="90",
                    wattage=120
                )
            ]
        )

        expected = Luminaire(
            gamma_angles=[],
            c_planes=[],
            intensity_values={},
            luminous_opening_geometry=None,
            geometry=None,
            lamps=[
                Lamps(
                    number_of_lamps=1,
                    description="Lamp 1",
                    lumens_per_lamp=1000,
                    wattage=100,
                    color="White",
                    cri="80"
                ),
                Lamps(
                    number_of_lamps=2,
                    description="Lamp 2",
                    lumens_per_lamp=700,
                    wattage=120,
                    color="Warm White",
                    cri="90"
                ),
            ],
            metadata=PhotometryMetadata(
                catalog_number=None,
                luminaire=None,
                manufacturer=None,
                date_and_user=None,
                file_source=None,
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=False,
                luminous_flux=Calculable(None),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(None)
            )
        )

        self.assertEqual(convert_content(content), expected)


if __name__ == '__main__':
    unittest.main()
