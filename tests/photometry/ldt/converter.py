import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape, LuminaireGeometry, Shape, \
    LuminaireType, Symmetry
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ldt.converter import convert_content
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


class TestConvertContent(unittest.TestCase):
    def test_empty_content(self):
        content = LdtContent()
        expected = Luminaire(
            photometry=LuminairePhotometricProperties(),
            metadata=PhotometryMetadata(
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS
            )
        )

        self.assertEqual(convert_content(content), expected)

    def test_full_luminaire(self):
        content = LdtContent(
            header="Manufacturer",
            type_indicator=1,
            symmetry_indicator=0,
            number_of_c_planes=2,
            distance_between_c_planes=45,
            number_of_intensities=5,
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
            c_angles=[0.0, 90.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4,
                1200.0, 1000.2, 950.0, 700.1, 328.4,
            ]
        )

        expected = Luminaire(
            luminous_opening_geometry=LuminousOpeningGeometry(
                length=1.0,
                width=0.5,
                height=0.3,
                height_c90=0.3,
                height_c180=0.3,
                height_c270=0.3,
                shape=LuminousOpeningShape.RECTANGULAR
            ),
            geometry=LuminaireGeometry(
                length=1,
                width=0.5,
                height=0.3,
                shape=Shape.RECTANGULAR
            ),
            lamps=[
                Lamps(
                    number_of_lamps=1,
                    description="Lamp 1",
                    lumens_per_lamp=1000,
                    wattage=100,
                    color="White",
                    cri="80"
                )
            ],
            metadata=PhotometryMetadata(
                catalog_number="Lum1",
                luminaire="Luminaire 1",
                manufacturer="Manufacturer",
                date_and_user="2024-03-10 Test User",
                measurement="MEAS1",
                file_source=None,
                filename="Lum1.ldt",
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS,
                luminaire_type=LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY,
                symmetry=Symmetry.NONE,
                conversion_factor=1.0,
                direct_ratios_for_room_indices={
                    0.60: 0.1,
                    0.80: 0.2,
                    1.00: 0.3,
                    1.25: 0.4,
                    1.50: 0.5,
                    2.00: 0.6,
                    2.50: 0.7,
                    3.00: 0.8,
                    4.00: 0.9,
                    5.00: 1
                }
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=False,
                luminous_flux=Calculable(None),
                lor=Calculable(1.0),
                dff=Calculable(1.0),
                efficacy=Calculable(None)
            ),
            c_planes=[0.0, 90.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensity_values={
                (0.0, 0.0): 2200.0,
                (0.0, 45.0): 2000.2,
                (0.0, 90.0): 1950.0,
                (0.0, 135.0): 1700.1,
                (0.0, 180.0): 1328.4,
                (90.0, 0.0): 1200.0,
                (90.0, 45.0): 1000.2,
                (90.0, 90.0): 950.0,
                (90.0, 135.0): 700.1,
                (90.0, 180.0): 328.4
            }
        )

        self.assertEqual(convert_content(content), expected)

    def test_symmetry(self):
        content = LdtContent(
            number_of_lamp_sets=1,
            lamp_sets=[
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Lamp 1",
                    total_lumens=1000.0,
                    light_color="White",
                    cri="80",
                    wattage=100
                )
            ],
            c_angles=[
                0, 45, 90, 135, 180,
                225, 270, 315, 360
            ],
            gamma_angles=[0.0, 90.0]
        )

        expected = Luminaire(
            lamps=[
                Lamps(
                    number_of_lamps=-1,
                    description="Lamp 1",
                    lumens_per_lamp=1000.0,
                    wattage=100,
                    color="White",
                    cri="80"
                )
            ],
            metadata=PhotometryMetadata(
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS,
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=True,
                luminous_flux=Calculable(500.0),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(5)
            ),
            gamma_angles=[
                0.0, 90.0
            ]
        )

        with self.subTest(title="No Symmetry"):
            content.symmetry_indicator = 0
            content.c_angles = [
                0, 15, 30, 45, 60
            ]

            content.intensities =  [
                2200.0, 2000.2,
                1950.0, 1700.1,
                1328.4, 1115.1,
                1328.4, 1115.1,
                1328.4, 1115.1
            ]

            expected.symmetry = Symmetry.NONE

            angle_combinations = [(c, gamma) for c in content.c_angles for gamma in content.gamma_angles]

            expected.intensity_values = {
                angle: content.intensities[i % len(content.intensities)]
                for i, angle
                in enumerate(angle_combinations)
            }

            actual = convert_content(content)

            for coord, value in expected.intensity_values.items():
                self.assertAlmostEqual(actual.intensity_values[coord], value, places=5,
                                       msg=f"Invalid value for coord {coord}")

        with self.subTest(title="Symmetry to vertical axis"):
            content.symmetry_indicator = 1
            content.c_angles=[
                0, 45, 90, 135, 180,
                225, 270, 315, 360
            ]
            content.intensities =  [2200.0, 2000.2]
            expected.symmetry = Symmetry.TO_VERTICAL_AXIS

            angle_combinations = [(c, gamma) for c in content.c_angles for gamma in content.gamma_angles]
            expected.intensity_values = {
                (0, 0): 2200.0,
                (0, 90): 2000.2,
                (45, 0): 2200.0,
                (45, 90): 2000.2,
                (90, 0): 2200.0,
                (90, 90): 2000.2,
                (135, 0): 2200.0,
                (135, 90): 2000.2,
                (180, 0): 2200.0,
                (180, 90): 2000.2,
                (225, 0): 2200.0,
                (225, 90): 2000.2,
                (270, 0): 2200.0,
                (270, 90): 2000.2,
                (315, 0): 2200.0,
                (315, 90): 2000.2
            }

            actual = convert_content(content)

            for coord, value in expected.intensity_values.items():
                self.assertAlmostEqual(actual.intensity_values[coord], value, places=5,
                                       msg=f"Invalid value for coord {coord}")

        with self.subTest(title="Symmetry to C0 C180"):
            content.symmetry_indicator = 2
            content.c_angles=[
                0, 45, 90, 135, 180,
                225, 270, 315, 360
            ]

            content.intensities = [
                2200.0, 400.0,
                2000.2, 300.0,
                1950.0, 200.0,
                1700.1, 100.0,
                1328.4, 50.0
            ]

            expected.symmetry = Symmetry.TO_C0_C180

            angle_combinations = [(c, gamma) for c in content.c_angles for gamma in content.gamma_angles]

            expected.intensity_values = {
                (0, 0): 2200.0,
                (0, 90): 400.0,
                (45, 0): 2000.2,
                (45, 90): 300.0,
                (90, 0): 1950.0,
                (90, 90): 200.0,
                (135, 0): 1700.1,
                (135, 90): 100.0,
                (180, 0): 1328.4,
                (180, 90): 50.0,

                (315, 0): 2000.2,
                (315, 90): 300.0,
                (270, 0): 1950.0,
                (270, 90): 200.0,
                (225, 0): 1700.1,
                (225, 90): 100.0
            }

            actual = convert_content(content)

            for coord, value in expected.intensity_values.items():
                self.assertAlmostEqual(actual.intensity_values[coord], value, places=5,
                                       msg=f"Invalid value for coord {coord}")


        with self.subTest(title="Symmetry to C90 C270"):
            content.symmetry_indicator = 3
            content.c_angles=[
                0, 45, 90, 135, 180,
                225, 270, 315, 360
            ]

            content.intensities = [
                2200.0, 400.0,
                2000.2, 300.0,
                1950.0, 200.0,
                1700.1, 100.0,
                1328.4, 50.0
            ]

            expected.symmetry = Symmetry.TO_C0_C180

            angle_combinations = [(c, gamma) for c in content.c_angles for gamma in content.gamma_angles]

            expected.intensity_values = {
                (270, 0): 2200.0,
                (270, 90): 400.0,
                (315, 0): 2000.2,
                (315, 90): 300.0,
                (0, 0): 1950.0,
                (0, 90): 200.0,
                (45, 0): 1700.1,
                (45, 90): 100.0,
                (90, 0): 1328.4,
                (90, 90): 50.0,

                (225, 0): 2000.2,
                (225, 90): 300.0,
                (180, 0): 1950.0,
                (180, 90): 200.0,
                (135, 0): 1700.1,
                (135, 90): 100.0,
            }

            actual = convert_content(content)

            for coord, value in expected.intensity_values.items():
                self.assertAlmostEqual(actual.intensity_values[coord], value, places=5,
                                       msg=f"Invalid value for coord {coord}")

        with self.subTest(title="Symmetry to C0 C180 C90 C270"):
            content.symmetry_indicator = 4
            content.c_angles=[
                0, 45, 90, 135, 180,
                225, 270, 315, 360
            ]
            content.intensities = [
                2200.0, 400.0,
                2000.2, 300.0,
                1950.0, 200.0,
            ]

            expected.symmetry = Symmetry.TO_C0_C180_C90_C270

            angle_combinations = [(c, gamma) for c in content.c_angles for gamma in content.gamma_angles]

            expected.intensity_values = {
                (0, 0): 2200.0,
                (0, 90): 400.0,
                (45, 0): 2000.2,
                (45, 90): 300.0,
                (90, 0): 1950.0,
                (90, 90): 200.0,

                (180, 0): 2200.0,
                (180, 90): 400.0,
                (135, 0): 2000.2,
                (135, 90): 300.0,

                (270, 0): 1950.0,
                (270, 90): 200.0,
                (315, 0): 2000.2,
                (315, 90): 300.0
            }

    def test_missing_values(self):
        cases = [
            {
                "title": "No symmetry",
                "symmetry_indicator": 0,
                "symmetry": Symmetry.NONE,
                "expected": {(0, 0): 1100.0}
            },
            {
                "title": "Symmetry to vertical axis",
                "symmetry_indicator": 1,
                "symmetry": Symmetry.TO_VERTICAL_AXIS,
                "expected": {(0, 0): 1100.0}
            },
            {
                "title": "Symmetry to C0 C180",
                "symmetry_indicator": 2,
                "symmetry": Symmetry.TO_C0_C180,
                "expected": {(0, 0): 1100.0}
            },
            {
                "title": "Symmetry to C90 C270",
                "symmetry_indicator": 3,
                "symmetry": Symmetry.TO_C90_C270,
                "expected": {}
            },
            {
                "title": "Symmetry to C0 C180 C90 C270",
                "symmetry_indicator": 4,
                "symmetry": Symmetry.TO_C0_C180_C90_C270,
                "expected": {(0, 0): 1100.0, (180, 0): 1100.0}
            }
        ]

        for case in cases:
            with self.subTest(title=case["title"]):
                content = LdtContent(
                    symmetry_indicator=case["symmetry_indicator"],
                    number_of_lamp_sets=1,
                    lamp_sets=[
                        LampSet(
                            number_of_lamps=-1,
                            type_of_lamp="Lamp 1",
                            total_lumens=500.0,
                            light_color="White",
                            cri="80",
                            wattage=100
                        )
                    ],
                    c_angles=[0.0],
                    gamma_angles=[
                        0.0, 45.0, 90.0, 135.0, 180.0
                    ],
                    intensities=[
                        2200.0
                    ]
                )

                expected = Luminaire(
                    lamps=[
                        Lamps(
                            number_of_lamps=1,
                            description="Lamp 1",
                            lumens_per_lamp=500.0,
                            wattage=100,
                            color="White",
                            cri="80"
                        )
                    ],
                    metadata=PhotometryMetadata(
                        file_format=FileFormat.LDT,
                        file_units=LengthUnits.MILLIMETERS,
                        symmetry=case["symmetry"]
                    ),
                    photometry=LuminairePhotometricProperties(
                        is_absolute=True,
                        luminous_flux=Calculable(500.0),
                        lor=Calculable(None),
                        dff=Calculable(None),
                        efficacy=Calculable(5)
                    ),
                    c_planes=[0.0],
                    gamma_angles=[
                        0.0, 45.0, 90.0, 135.0, 180.0
                    ],
                    intensity_values=case["expected"]
                )

                self.assertEqual(convert_content(content), expected)

    def test_absolute_photometry(self):
        content = LdtContent(
            number_of_lamp_sets=1,
            lamp_sets=[
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Lamp 1",
                    total_lumens=500,
                    light_color="White",
                    cri="80",
                    wattage=100
                )
            ],
            c_angles=[0.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensities=[
                2200.0, 2000.0, 1200.0, 1000.0, 200.0
            ]
        )

        expected = Luminaire(
            lamps=[
                Lamps(
                    number_of_lamps=1,
                    description="Lamp 1",
                    lumens_per_lamp=500,
                    wattage=100,
                    color="White",
                    cri="80"
                )
            ],
            metadata=PhotometryMetadata(
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS,
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=True,
                luminous_flux=Calculable(500),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(5)
            ),
            c_planes=[0.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensity_values={
                (0.0, 0.0): 1100.0,
                (0.0, 45.0): 1000.0,
                (0.0, 90.0): 600.0,
                (0.0, 135.0): 500.0,
                (0.0, 180.0): 100.0,
            }
        )

        self.assertEqual(convert_content(content), expected)

    def test_relative_photometry(self):
        content = LdtContent(
            number_of_lamp_sets=1,
            lamp_sets=[
                LampSet(
                    number_of_lamps=2,
                    type_of_lamp="Lamp 1",
                    total_lumens=500,
                    light_color="White",
                    cri="80",
                    wattage=100
                )
            ],
            c_angles=[0.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4
            ]
        )

        expected = Luminaire(
            lamps=[
                Lamps(
                    number_of_lamps=2,
                    description="Lamp 1",
                    lumens_per_lamp=250.0,
                    wattage=100,
                    color="White",
                    cri="80"
                )
            ],
            metadata=PhotometryMetadata(
                file_format=FileFormat.LDT,
                file_units=LengthUnits.MILLIMETERS,
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=False,
                luminous_flux=Calculable(None),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(None)
            ),
            c_planes=[0.0],
            gamma_angles=[
                0.0, 45.0, 90.0, 135.0, 180.0
            ],
            intensity_values={
                (0.0, 0.0): 2200.0,
                (0.0, 45.0): 2000.2,
                (0.0, 90.0): 1950.0,
                (0.0, 135.0): 1700.1,
                (0.0, 180.0): 1328.4
            }
        )

        self.assertEqual(convert_content(content), expected)

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
