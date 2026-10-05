import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape, LuminaireGeometry, Shape, \
    LuminaireType, Symmetry
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.iesna_common.model import Attribute
from photometric_viewer.photometry.ldt.converter import convert_content
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


def default_content() -> LdtContent:
    return LdtContent(
        header=Attribute("Manufacturer", line=1),
        type_indicator=Attribute("1" , line=1),
        symmetry_indicator=Attribute("0" , line=1),
        number_of_c_planes=Attribute("2" , line=1),
        distance_between_c_planes=Attribute("45" , line=1),
        number_of_intensities=Attribute("5" , line=1),
        distance_between_intensities=Attribute("2.5" , line=1),
        measurement_report=Attribute("MEAS1" , line=1),
        luminaire_name=Attribute("Luminaire 1" , line=1),
        luminaire_number=Attribute("Lum1" , line=1),
        file_name=Attribute("Lum1.ldt" , line=1),
        date_and_user=Attribute("2024-03-10 Test User" , line=1),
        length_of_luminaire=Attribute("1000" , line=1),
        width_of_luminaire=Attribute("500" , line=1),
        height_of_luminaire=Attribute("300" , line=1),
        length_of_luminous_area=Attribute("1000" , line=1),
        width_of_luminous_area=Attribute("500" , line=1),
        height_of_luminous_area_c0=Attribute("300" , line=1),
        height_of_luminous_area_c90=Attribute("300" , line=1),
        height_of_luminous_area_c180=Attribute("300" , line=1),
        height_of_luminous_area_c270=Attribute("300" , line=1),
        dff_percent=Attribute("100" , line=1),
        lor_percent=Attribute("100" , line=1),
        conversion_factor=Attribute("1.0" , line=1),
        tilt=Attribute("0", line=1),
        number_of_lamp_sets=Attribute("1", line=1),
        lamp_sets=[
            LampSet(
                number_of_lamps=Attribute("1", line=1),
                type_of_lamp=Attribute("Lamp 1", line=1),
                total_lumens=Attribute("1000", line=1),
                light_color=Attribute("White", line=1),
                cri=Attribute("80", line=1),
                wattage=Attribute("100", line=1),
            )
        ],
        direct_ratios_for_room_indices=[
            Attribute(str(v), line=1) for v in [
                0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1
            ]
        ],
        c_angles=[ Attribute(str(v), line=1) for v in [0.0, 90.0]],
        gamma_angles=[
            Attribute(str(v), line=1) for v in [
                0.0, 45.0, 90.0, 135.0, 180.0
            ]
        ],
        intensities=[
            Attribute(str(v), line=1) for v in [
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4,
                1200.0, 1000.2, 950.0, 700.1, 328.4
            ]
        ]
    )

class TestConvertContent(unittest.TestCase):
    def test_empty_lamp(self):
        content = default_content()
        content.lamp_sets =  [
            LampSet(
                    number_of_lamps=Attribute(None, line=1),
                    type_of_lamp=Attribute(None, line=1),
                    total_lumens=Attribute(None, line=1),
                    light_color=Attribute(None, line=1),
                    cri=Attribute(None, line=1),
                    wattage=Attribute(None, line=1)
            )
        ]

        expected = [Lamps(number_of_lamps=None)]

        self.assertEqual(convert_content(content).lamps, expected)

    def test_full_luminaire(self):
        content = default_content()

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
                length=1.0,
                width=0.5,
                height=0.3,
                shape=Shape.RECTANGULAR
            ),
            lamps=[
                Lamps(
                    number_of_lamps=1,
                    description="Lamp 1",
                    lumens_per_lamp=1000.0,
                    wattage=100.0,
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
                filename="Lum1.ldt",
                file_format=FileFormat.EULUMDAT,
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
                    5.00: 1.0
                }
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=False,
                luminous_flux=Calculable(None),
                lor=Calculable(None),
                dff=Calculable(None),
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

    def test_no_symmetry(self):
        content = default_content()
        content.intensities = [
            Attribute(str(v), line=1) for v in [
                2000.0, 1000.0,
                2100.0, 1100.0,
                2200.0, 1200.0,
                2300.0, 1300.0,
                2400.0, 1400.0
            ]
        ]
        content.symmetry_indicator=Attribute("0", line=1)
        content.c_angles = [
            Attribute("0.0", line=1),
            Attribute("10.0", line=1),
            Attribute("20.0", line=1),
            Attribute("30.0", line=1),
            Attribute("180.0", line=1)
        ]
        content.gamma_angles = [
            Attribute("0.0", line=1),
            Attribute("90.0", line=1)
        ]
        content.intensities = [
            Attribute(str(v), line=1) for v in [
                2000.0, 1000.0,
                2100.0, 1100.0,
                2200.0, 1200.0,
                2300.0, 1300.0,
                2400.0, 1400.0
            ]
        ]

        expected_intensity_values = {
                (0.0, 0.0): 2000.0,
                (0.0, 90.0): 1000.0,
                (10.0, 0.0): 2100.0,
                (10.0, 90.0): 1100.0,
                (20.0, 0.0): 2200.0,
                (20.0, 90.0): 1200.0,
                (30.0, 0.0): 2300.0,
                (30.0, 90.0): 1300.0,
                (180.0, 0.0): 2400.0,
                (180.0, 90.0): 1400.0,
        }

        expected_c_angles = [0.0, 10.0, 20.0, 30.0, 180.0]


        actual = convert_content(content)

        self.assertEqual(actual.intensity_values, expected_intensity_values)
        self.assertEqual(actual.c_planes, expected_c_angles)

    def test_symmetry_to_vertical_axis(self):
        content = default_content()
        content.symmetry_indicator=Attribute("1", line=1)
        content.c_angles=[
            Attribute(str(v), line=1) for v in
            [
                0.0, 45.0, 90.0, 135.0, 180.0,
                225.0, 270.0, 315.0
            ]
        ]

        content.gamma_angles=[
            Attribute(str(v), line=1) for v in [0.0, 90.0]
        ]
        content.intensities=[Attribute(str(v), line=1) for v in [2000.0, 1000.0]]

        expected_c_planes = [
            0.0, 45.0, 90.0, 135.0, 180.0,
            225.0, 270.0, 315.0
        ]

        expected_intensity_values = {
                (0.0, 0.0): 2000.0,
                (0.0, 90.0): 1000.0,
                (45.0, 0.0): 2000.0,
                (45.0, 90.0): 1000.0,
                (90.0, 0.0): 2000.0,
                (90.0, 90.0): 1000.0,
                (135.0, 0.0): 2000.0,
                (135.0, 90.0): 1000.0,
                (180.0, 0.0): 2000.0,
                (180.0, 90.0): 1000.0,
                (225.0, 0.0): 2000.0,
                (225.0, 90.0): 1000.0,
                (270.0, 0.0): 2000.0,
                (270.0, 90.0): 1000.0,
                (315.0, 0.0): 2000.0,
                (315.0, 90.0): 1000.0
        }

        actual = convert_content(content)

        self.assertEqual(actual.intensity_values, expected_intensity_values)
        self.assertEqual(actual.metadata.symmetry, Symmetry.TO_VERTICAL_AXIS)
        self.assertEqual(actual.c_planes, expected_c_planes)

    def test_symmetry_to_c0_c180(self):
        content = default_content()
        content.symmetry_indicator=Attribute("2", line=1)
        content.c_angles = [
            Attribute(str(v), line=1) for v in
            [
                0.0, 45.0, 90.0, 135.0, 180.0,
                225.0, 270.0, 315.0, 360.0
            ]
        ]
        content.gamma_angles = [
            Attribute(str(v), line=1) for v in
            [0.0, 90.0]
        ]
        content.intensities = [
            Attribute(str(v), line=1) for v in
            [ 2000.0, 1000.0, 2100.0, 1100.0, 2200.0, 1200.0, 2300.0, 1300.0, 2400.0, 1400.0 ]
        ]

        expected_c_planes = [
            0.0, 45.0, 90.0, 135.0, 180.0,
            225.0, 270.0, 315.0, 360.0
        ]

        expected_intensity_values = {
            (0.0, 0.0): 2000.0,
            (0.0, 90.0): 1000.0,
            (45.0, 0.0): 2100.0,
            (45.0, 90.0): 1100.0,
            (90.0, 0.0): 2200.0,
            (90.0, 90.0): 1200.0,
            (135.0, 0.0): 2300.0,
            (135.0, 90.0): 1300.0,
            (180.0, 0.0): 2400.0,
            (180.0, 90.0): 1400.0,

            (315.0, 0.0): 2100.0,
            (315.0, 90.0): 1100.0,
            (270.0, 0.0): 2200.0,
            (270.0, 90.0): 1200.0,
            (225.0, 0.0): 2300.0,
            (225.0, 90.0): 1300.0
        }

        actual = convert_content(content)

        self.assertEqual(actual.intensity_values, expected_intensity_values)
        self.assertEqual(actual.metadata.symmetry, Symmetry.TO_C0_C180)
        self.assertEqual(actual.c_planes, expected_c_planes)


    def test_symmetry_to_c90_c270(self):
        content = default_content()
        content.symmetry_indicator = Attribute("3", line=1)

        content.c_angles = [
            Attribute(str(v), line=1) for v in
            [
                0.0, 45.0, 90.0, 135.0, 180.0,
                225.0, 270.0, 315.0, 360.0
            ]
        ]

        content.gamma_angles = [
            Attribute(str(v), line=1) for v in
            [0.0, 90.0]
        ]

        content.intensities = [
            Attribute(str(v), line=1) for v in
            [
                2000.0, 1000.0,
                2100.0, 1100.0,
                2200.0, 1200.0,
                2300.0, 1300.0,
                2400.0, 1400.0
            ]
        ]

        expected_c_planes = [
            0.0, 45.0, 90.0, 135.0, 180.0,
            225.0, 270.0, 315.0, 360.0
        ]

        expected_intensity_values= {
            (270, 0): 2000.0,
            (270, 90): 1000.0,
            (315, 0): 2100.0,
            (315, 90): 1100.0,
            (0, 0): 2200.0,
            (0, 90): 1200.0,
            (45, 0): 2300.0,
            (45, 90): 1300.0,
            (90, 0): 2400.0,
            (90, 90): 1400.0,

            (225, 0): 2100.0,
            (225, 90): 1100.0,
            (180, 0): 2200.0,
            (180, 90): 1200.0,
            (135, 0): 2300.0,
            (135, 90): 1300.0,
        }


        actual = convert_content(content)

        self.assertEqual(actual.intensity_values, expected_intensity_values)
        self.assertEqual(actual.metadata.symmetry, Symmetry.TO_C90_C270)
        self.assertEqual(actual.c_planes, expected_c_planes)

    def test_symmetry_to_c0_c180_c90_c270(self):
        content = default_content()
        content.symmetry_indicator = Attribute("4", line=1)
        content.c_angles = [
            Attribute(str(v), line=1) for v in
            [
                0.0, 45.0, 90.0, 135.0, 180.0,
                225.0, 270.0, 315.0, 360.0
            ]
        ]
        content.gamma_angles = [
            Attribute(str(v), line=1) for v in
            [
                0.0, 90.0
            ]
        ]

        content.intensities = [
            Attribute(str(v), line=1) for v in
            [
                2000.0, 1000.0,
                2100.0, 1100.0,
                2200.0, 1200.0
            ]
        ]

        expected_c_planes=[
            0.0, 45.0, 90.0, 135.0, 180.0,
            225.0, 270.0, 315.0, 360.0
        ]

        expected_intensity_values={
            (0.0, 0.0): 2000.0,
            (0.0, 90.0): 1000.0,
            (45.0, 0.0): 2100.0,
            (45.0, 90.0): 1100.0,
            (90.0, 0.0): 2200.0,
            (90.0, 90.0): 1200.0,

            (135.0, 0.0): 2100.0,
            (135.0, 90.0): 1100.0,
            (180.0, 0.0): 2000.0,
            (180.0, 90.0): 1000.0,

            (225.0, 0.0): 2100.0,
            (225.0, 90.0): 1100.0,
            (270.0, 0.0): 2200.0,
            (270.0, 90.0): 1200.0,

            (315.0, 0.0): 2100.0,
            (315.0, 90.0): 1100.0
        }

        actual = convert_content(content)

        self.assertEqual(actual.intensity_values, expected_intensity_values)
        self.assertEqual(actual.metadata.symmetry, Symmetry.TO_C0_C180_C90_C270)
        self.assertEqual(actual.c_planes, expected_c_planes)

    def test_missing_values(self):
        cases = [
            {
                "title": "No symmetry",
                "symmetry_indicator": 0,
                "symmetry": Symmetry.NONE,
                "expected": {(0.0, 0.0): 1100.0}
            },
            {
                "title": "Symmetry to vertical axis",
                "symmetry_indicator": 1,
                "symmetry": Symmetry.TO_VERTICAL_AXIS,
                "expected": {
                    (0.0, 0.0): 1100.0,
                    (90.0, 0.0): 1100.0,
                    (180.0, 0.0): 1100.0,
                    (270.0, 0.0): 1100.0,
                    (360.0, 0.0): 1100.0
                }
            },
            {
                "title": "Symmetry to C0 C180",
                "symmetry_indicator": 2,
                "symmetry": Symmetry.TO_C0_C180,
                "expected": {(0.0, 0.0): 1100.0}
            },
            {
                "title": "Symmetry to C90 C270",
                "symmetry_indicator": 3,
                "symmetry": Symmetry.TO_C90_C270,
                "expected": {(270.0, 0.0): 1100.0}
            },
            {
                "title": "Symmetry to C0 C180 C90 C270",
                "symmetry_indicator": 4,
                "symmetry": Symmetry.TO_C0_C180_C90_C270,
                "expected": {(0.0, 0.0): 1100.0, (180.0, 0.0): 1100.0}
            }
        ]

        for case in cases:
            with (self.subTest(title=case["title"])):
                content = default_content()
                content.c_angles=[
                    Attribute(str(x), line=1)
                    for x in [0.0, 90.0, 180.0, 270.0, 360.0]
                ]
                content.gamma_angles=[
                    Attribute(str(x), line=1)
                    for x in [0.0, 45.0, 90.0, 135.0, 180.0]
                ]
                content.lamp_sets = [
                    LampSet(
                        number_of_lamps=Attribute("-1", line=1),
                        type_of_lamp=Attribute("Lamp 1", line=1),
                        total_lumens=Attribute("500", line=1),
                        light_color=Attribute("White", line=1),
                        cri=Attribute("80", line=1),
                        wattage=Attribute("100", line=1),
                    )
                ]
                content.symmetry_indicator = Attribute(str(case["symmetry_indicator"]), line=1)
                content.intensities = [Attribute("2200.0", line=1)]
                self.assertEqual(convert_content(content).intensity_values, case["expected"])

    def test_absolute_photometry(self):
        content = default_content()
        content.number_of_lamp_sets=Attribute("1", line=1)
        content.lamp_sets=[
            LampSet(
                number_of_lamps=Attribute("-1", line=1),
                type_of_lamp=Attribute("Lamp 1", line=1),
                total_lumens=Attribute("500", line=1),
                light_color=Attribute("White", line=1),
                cri=Attribute("80", line=1),
                wattage=Attribute("100", line=1),
            )
        ]
        content.c_angles=[
            Attribute("0.0", line=1)
        ]
        content.gamma_angles=[
            Attribute(str(x), line=1)
            for x in [0.0, 45.0, 90.0, 135.0, 180.0]
        ]
        content.intensities=[
            Attribute(str(x), line=1)
            for x in [2200.0, 2000.0, 1200.0, 1000.0, 200.0]
        ]


        expected_lamps = [
            Lamps(
                number_of_lamps=1,
                description="Lamp 1",
                lumens_per_lamp=500,
                wattage=100,
                color="White",
                cri="80"
            )
        ]

        expected_photometry=LuminairePhotometricProperties(
            is_absolute=True,
            luminous_flux=Calculable(500),
            lor=Calculable(None),
            dff=Calculable(None),
            efficacy=Calculable(5)
        )

        expected_c_planes=[0.0]
        expected_gamma_angles=[
            0.0, 45.0, 90.0, 135.0, 180.0
        ]

        expected_intensity_values={
            (0.0, 0.0): 1100.0,
            (0.0, 45.0): 1000.0,
            (0.0, 90.0): 600.0,
            (0.0, 135.0): 500.0,
            (0.0, 180.0): 100.0,
        }

        actual = convert_content(content)

        self.assertEqual(actual.lamps, expected_lamps)
        self.assertEqual(actual.photometry, expected_photometry)
        self.assertEqual(actual.c_planes, expected_c_planes)
        self.assertEqual(actual.gamma_angles, expected_gamma_angles)
        self.assertEqual(actual.intensity_values, expected_intensity_values)

    def test_relative_photometry(self):
        content = default_content()
        content.number_of_lamp_sets=Attribute("1", line=1)
        content.lamp_sets=[
            LampSet(
                number_of_lamps=Attribute("2", line=1),
                type_of_lamp=Attribute("Lamp 1", line=1),
                total_lumens=Attribute("500", line=1),
                light_color=Attribute("White", line=1),
                cri=Attribute("80", line=1),
                wattage=Attribute("100", line=1),
            )
        ]
        content.c_angles=[
            Attribute("0.0", line=1)
        ]
        content.gamma_angles=[
            Attribute(str(x), line=1)
            for x in [0.0, 45.0, 90.0, 135.0, 180.0]
        ]
        content.intensities=[
            Attribute(str(x), line=1)
            for x in [2200.0, 2000.2, 1950.0, 1700.1, 1328.4]
        ]


        expected_lamps = [
            Lamps(
                number_of_lamps=2,
                description="Lamp 1",
                lumens_per_lamp=250.0,
                wattage=100,
                color="White",
                cri="80"
            )
        ]

        expected_photometry=LuminairePhotometricProperties(
            is_absolute=False,
            luminous_flux=Calculable(None),
            lor=Calculable(None),
            dff=Calculable(None),
            efficacy=Calculable(None)
        )

        expected_c_planes=[0.0]
        expected_gamma_angles=[
            0.0, 45.0, 90.0, 135.0, 180.0
        ]

        expected_intensity_values={
            (0.0, 0.0): 2200.0,
            (0.0, 45.0): 2000.2,
            (0.0, 90.0): 1950.0,
            (0.0, 135.0): 1700.1,
            (0.0, 180.0): 1328.4
        }

        actual = convert_content(content)

        self.assertEqual(actual.lamps, expected_lamps)
        self.assertEqual(actual.photometry, expected_photometry)
        self.assertEqual(actual.c_planes, expected_c_planes)
        self.assertEqual(actual.gamma_angles, expected_gamma_angles)
        self.assertEqual(actual.intensity_values, expected_intensity_values)

    def test_luminous_opening_geometry(self):
        test_cases = [
            {
                "title": "Point",
                "dimensions": (0, 0, 0, 0, 0, 0),
                "expected": LuminousOpeningGeometry(
                    length=0.0,
                    width=0.0,
                    height=0.0,
                    height_c90=0.0,
                    height_c180=0.0,
                    height_c270=0.0,
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
                content = default_content()
                content.length_of_luminous_area = Attribute(str(case["dimensions"][0]), line=1)
                content.width_of_luminous_area = Attribute(str(case["dimensions"][1]), line=1)
                content.height_of_luminous_area_c0 = Attribute(str(case["dimensions"][2]), line=1)
                content.height_of_luminous_area_c90 = Attribute(str(case["dimensions"][3]), line=1)
                content.height_of_luminous_area_c180 = Attribute(str(case["dimensions"][4]), line=1)
                content.height_of_luminous_area_c270 = Attribute(str(case["dimensions"][5]), line=1)

                self.assertEqual(convert_content(content).luminous_opening_geometry, case["expected"])

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
                content = default_content()
                content.length_of_luminaire = Attribute(str(case["dimensions"][0]), line=1)
                content.width_of_luminaire = Attribute(str(case["dimensions"][1]), line=1)
                content.height_of_luminaire = Attribute(str(case["dimensions"][2]), line=1)
                self.assertEqual(convert_content(content).geometry, case["expected"])

    def test_multiple_lamp_sets(self):
        content = default_content()
        content.number_of_lamp_sets=Attribute("2", line=1)
        content.lamp_sets=[
            LampSet(
                number_of_lamps=Attribute("1", line=1),
                type_of_lamp=Attribute("Lamp 1", line=1),
                total_lumens=Attribute("1000", line=1),
                light_color=Attribute("White", line=1),
                cri=Attribute("80", line=1),
                wattage=Attribute("100", line=1),
            ),
            LampSet(
                number_of_lamps=Attribute("2", line=1),
                type_of_lamp=Attribute("Lamp 2", line=1),
                total_lumens=Attribute("1400", line=1),
                light_color=Attribute("Warm White", line=1),
                cri=Attribute("90", line=1),
                wattage=Attribute("120", line=1),
            )
        ]

        expected = [
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
                )
            ]

        self.assertEqual(convert_content(content).lamps, expected)


if __name__ == '__main__':
    unittest.main()
