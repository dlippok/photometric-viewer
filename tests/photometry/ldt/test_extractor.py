import io
import unittest

from photometric_viewer.photometry.iesna_common.model import Attribute
from photometric_viewer.photometry.ldt.extractor import extract_content
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


class TestExtractContent(unittest.TestCase):
    def test_full_file(self):
        content = """ACME Inc.
            0
            0
            1
            0
            37
            0
            MEAS1234
            Dummy LDT file. Can be used for testing, creating screenshots, etc.
            BD0150
            dummy.ldt
            2023-05-01
            750
            0
            0.0
            750.0
            0
            10.0
            20.0
            30.0
            40.0
            100
            100
            1
            0
            1
            -1
            Generic 15W LED module
            1000
            3600K
            90
            15.0
            0.1
            0.2
            0.3
            0.4
            0.5
            0.6
            0.7
            0.8
            0.9
            0.11
            0.0
            0.0
            2.5
            5.0
            7.5
            10.0
            12.5
            15.0
            17.5
            20.0
            22.5
            25.0
            27.5
            30.0
            32.5
            35.0
            37.5
            40.0
            42.5
            45.0
            47.5
            50.0
            52.5
            55.0
            57.5
            60.0
            62.5
            65.0
            67.5
            70.0
            72.5
            75.0
            77.5
            80.0
            82.5
            85.0
            87.5
            90.0
            2200.0
            2000.2
            1950.0
            1700.1
            1328.4
            1115.1
            900.5
            700.4
            600.3
            501.2
            400.1
            398.3
            380.9
            400.2
            390.5
            320.0
            185.0
            100.6
            40.1
            20.0
            15.2
            15.0
            14.0
            11.0
            10.8
            10.8
            10.0
            7.0
            4.0
            1.2
            0.0
            0.0
            0.0
            0.0
            0.0
            1.0
            0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = LdtContent(
            header=Attribute("ACME Inc.", line=1),
            type_indicator=Attribute("0", line=2),
            symmetry_indicator=Attribute("0", line=3),
            number_of_c_planes=Attribute("1", line=4),
            distance_between_c_planes=Attribute("0", line=5),
            number_of_intensities=Attribute("37", line=6),
            distance_between_intensities=Attribute("0", line=7),
            measurement_report=Attribute("MEAS1234", line=8),
            luminaire_name=Attribute("Dummy LDT file. Can be used for testing, creating screenshots, etc.", line=9),
            luminaire_number=Attribute("BD0150", line=10),
            file_name=Attribute("dummy.ldt", line=11),
            date_and_user=Attribute("2023-05-01", line=12),
            length_of_luminaire=Attribute("750", line=13),
            width_of_luminaire=Attribute("0", line=14),
            height_of_luminaire=Attribute("0.0", line=15),
            length_of_luminous_area=Attribute("750.0", line=16),
            width_of_luminous_area=Attribute("0", line=17),
            height_of_luminous_area_c0=Attribute("10.0", line=18),
            height_of_luminous_area_c90=Attribute("20.0", line=19),
            height_of_luminous_area_c180=Attribute("30.0", line=20),
            height_of_luminous_area_c270=Attribute("40.0", line=21),
            dff_percent=Attribute("100", line=22),
            lor_percent=Attribute("100", line=23),
            conversion_factor=Attribute("1", line=24),
            tilt=Attribute("0", line=25),
            number_of_lamp_sets=Attribute("1", line=26),
            lamp_sets=[
                LampSet(
                    number_of_lamps=Attribute("-1", line=27),
                    type_of_lamp=Attribute("Generic 15W LED module", line=28),
                    total_lumens=Attribute("1000", line=29),
                    light_color=Attribute("3600K", line=30),
                    cri=Attribute('90', line=31),
                    wattage=Attribute("15.0", line=32)
                )
            ],
            direct_ratios_for_room_indices= [
                Attribute(str(x[1]), line=x[0]+33) for x
                in enumerate([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11])
            ],
            c_angles=[
                Attribute("0.0", line=43)
            ],
            gamma_angles=[
                Attribute(str(x[1]), line=x[0]+44)
                for x
                in enumerate(
                    [
                        0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                        32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                        65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
                    ]
                )
            ],
            intensities=[
                Attribute(str(x[1]), line=x[0]+81)
                for x
                in enumerate(
                    [
                        2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2,
                        400.1, 398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0,
                        14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
                    ]
                )
            ]
        )

        self.assertEqual(extracted, expected)

    def test_missing_intensities(self):
        content = """ACME Inc.
                    0
                    0
                    1
                    0
                    37
                    0
                    MEAS1234
                    Dummy LDT file. Can be used for testing, creating screenshots, etc.
                    BD0150
                    dummy.ldt
                    2023-05-01
                    750
                    0
                    0.0
                    750.0
                    0
                    10.0
                    20.0
                    30.0
                    40.0
                    100
                    100
                    1
                    0
                    1
                    -1
                    Generic 15W LED module
                    1000
                    3600K
                    90
                    15.0
                    0.1
                    0.2
                    0.3
                    0.4
                    0.5
                    0.6
                    0.7
                    0.8
                    0.9
                    0.11
                    0.0
                    0.0
                    2.5
                    5.0
                    7.5
                    10.0
                    12.5
                    15.0
                    17.5
                    20.0
                    22.5
                    25.0
                    27.5
                    30.0
                    32.5
                    35.0
                    37.5
                    40.0
                    42.5
                    45.0
                    47.5
                    50.0
                    52.5
                    55.0
                    57.5
                    60.0
                    62.5
                    65.0
                    67.5
                    70.0
                    72.5
                    75.0
                    77.5
                    80.0
                    82.5
                    85.0
                    87.5
                    90.0
                    2200.0
                    2000.2
                """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = LdtContent(
            header=Attribute("ACME Inc.", line=1),
            type_indicator=Attribute("0", line=2),
            symmetry_indicator=Attribute("0", line=3),
            number_of_c_planes=Attribute("1", line=4),
            distance_between_c_planes=Attribute("0", line=5),
            number_of_intensities=Attribute("37", line=6),
            distance_between_intensities=Attribute("0", line=7),
            measurement_report=Attribute("MEAS1234", line=8),
            luminaire_name=Attribute("Dummy LDT file. Can be used for testing, creating screenshots, etc.", line=9),
            luminaire_number=Attribute("BD0150", line=10),
            file_name=Attribute("dummy.ldt", line=11),
            date_and_user=Attribute("2023-05-01", line=12),
            length_of_luminaire=Attribute("750", line=13),
            width_of_luminaire=Attribute("0", line=14),
            height_of_luminaire=Attribute("0.0", line=15),
            length_of_luminous_area=Attribute("750.0", line=16),
            width_of_luminous_area=Attribute("0", line=17),
            height_of_luminous_area_c0=Attribute("10.0", line=18),
            height_of_luminous_area_c90=Attribute("20.0", line=19),
            height_of_luminous_area_c180=Attribute("30.0", line=20),
            height_of_luminous_area_c270=Attribute("40.0", line=21),
            dff_percent=Attribute("100", line=22),
            lor_percent=Attribute("100", line=23),
            conversion_factor=Attribute("1", line=24),
            tilt=Attribute("0", line=25),
            number_of_lamp_sets=Attribute("1", line=26),
            lamp_sets=[
                LampSet(
                    number_of_lamps=Attribute("-1", line=27),
                    type_of_lamp=Attribute("Generic 15W LED module", line=28),
                    total_lumens=Attribute("1000", line=29),
                    light_color=Attribute("3600K", line=30),
                    cri=Attribute('90', line=31),
                    wattage=Attribute("15.0", line=32)
                )
            ],
            direct_ratios_for_room_indices=[
                Attribute(str(x[1]), line=x[0] + 33) for x
                in enumerate([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11])
            ],
            c_angles=[
                Attribute("0.0", line=43)
            ],
            gamma_angles=[
                Attribute(str(x[1]), line=x[0] + 44)
                for x
                in enumerate(
                    [
                        0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                        32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                        65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
                    ]
                )
            ],
            intensities=[
                Attribute(str(x[1]), line=x[0] + 81)
                for x
                in enumerate(
                    [
                        2200.0, 2000.2
                    ]
                )
            ]
        )

        self.assertEqual(extracted, expected)

    def test_multiple_lamp_sets(self):
        content = """ACME Inc.
            0
            0
            1
            0
            37
            0
            MEAS1234
            Dummy LDT file. Can be used for testing, creating screenshots, etc.
            BD0150
            dummy.ldt
            2023-05-01
            750
            0
            0.0
            750.0
            0
            10.0
            20.0
            30.0
            40.0
            100
            100
            1
            0
            2
            -1
            Set 1
            1000
            3600K
            90
            20.0
            -1
            Set 2
            500
            3000K
            80
            15.0
            0.1
            0.2
            0.3
            0.4
            0.5
            0.6
            0.7
            0.8
            0.9
            0.11
            0.0
            0.0
            2.5
            5.0
            7.5
            10.0
            12.5
            15.0
            17.5
            20.0
            22.5
            25.0
            27.5
            30.0
            32.5
            35.0
            37.5
            40.0
            42.5
            45.0
            47.5
            50.0
            52.5
            55.0
            57.5
            60.0
            62.5
            65.0
            67.5
            70.0
            72.5
            75.0
            77.5
            80.0
            82.5
            85.0
            87.5
            90.0
            2200.0
            2000.2
            1950.0
            1700.1
            1328.4
            1115.1
            900.5
            700.4
            600.3
            501.2
            400.1
            398.3
            380.9
            400.2
            390.5
            320.0
            185.0
            100.6
            40.1
            20.0
            15.2
            15.0
            14.0
            11.0
            10.8
            10.8
            10.0
            7.0
            4.0
            1.2
            0.0
            0.0
            0.0
            0.0
            0.0
            1.0
            0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = LdtContent(
            header=Attribute("ACME Inc.", line=1),
            type_indicator=Attribute("0", line=2),
            symmetry_indicator=Attribute("0", line=3),
            number_of_c_planes=Attribute("1", line=4),
            distance_between_c_planes=Attribute("0", line=5),
            number_of_intensities=Attribute("37", line=6),
            distance_between_intensities=Attribute("0", line=7),
            measurement_report=Attribute("MEAS1234", line=8),
            luminaire_name=Attribute("Dummy LDT file. Can be used for testing, creating screenshots, etc.", line=9),
            luminaire_number=Attribute("BD0150", line=10),
            file_name=Attribute("dummy.ldt", line=11),
            date_and_user=Attribute("2023-05-01", line=12),
            length_of_luminaire=Attribute("750", line=13),
            width_of_luminaire=Attribute("0", line=14),
            height_of_luminaire=Attribute("0.0", line=15),
            length_of_luminous_area=Attribute("750.0", line=16),
            width_of_luminous_area=Attribute("0", line=17),
            height_of_luminous_area_c0=Attribute("10.0", line=18),
            height_of_luminous_area_c90=Attribute("20.0", line=19),
            height_of_luminous_area_c180=Attribute("30.0", line=20),
            height_of_luminous_area_c270=Attribute("40.0", line=21),
            dff_percent=Attribute("100", line=22),
            lor_percent=Attribute("100", line=23),
            conversion_factor=Attribute("1", line=24),
            tilt=Attribute("0", line=25),
            number_of_lamp_sets=Attribute("2", line=26),
            lamp_sets=[
                LampSet(
                    number_of_lamps=Attribute("-1", line=27),
                    type_of_lamp=Attribute("Set 1", line=28),
                    total_lumens=Attribute("1000", line=29),
                    light_color=Attribute("3600K", line=30),
                    cri=Attribute('90', line=31),
                    wattage=Attribute("20.0", line=32)
                ),
                LampSet(
                    number_of_lamps=Attribute("-1", line=33),
                    type_of_lamp=Attribute("Set 2", line=34),
                    total_lumens=Attribute("500", line=35),
                    light_color=Attribute("3000K", line=36),
                    cri=Attribute('80', line=37),
                    wattage=Attribute("15.0", line=38)
                ),
            ],
            direct_ratios_for_room_indices=[
                Attribute(str(x[1]), line=x[0] + 39) for x
                in enumerate([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11])
            ],
            c_angles=[
                Attribute("0.0", line=49)
            ],
            gamma_angles=[
                Attribute(str(x[1]), line=x[0] + 50)
                for x
                in enumerate(
                    [
                        0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                        32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                        65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
                    ]
                )
            ],
            intensities=[
                Attribute(str(x[1]), line=x[0] + 87)
                for x
                in enumerate(
                    [
                        2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2,
                        400.1, 398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0,
                        14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
                    ]
                )
            ]
        )

        self.assertEqual(extracted, expected)

if __name__ == '__main__':
    unittest.main()
