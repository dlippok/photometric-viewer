import io
import unittest

from photometric_viewer.photometry.ldt.extractor import extract_content
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet


class TestExtractContent(unittest.TestCase):
    def test_empty_file(self):
        content = ""

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = LdtContent(
            header=None,
            type_indicator=None,
            symmetry_indicator=None,
            distance_between_c_planes=None,
            number_of_intensities=None,
            distance_between_intensities=None,
            measurement_report=None,
            luminaire_name=None,
            luminaire_number=None,
            file_name=None,
            date_and_user=None,
            length_of_luminaire=None,
            width_of_luminaire=None,
            height_of_luminaire=None,
            length_of_luminous_area=None,
            width_of_luminous_area=None,
            height_of_luminous_area_c0=None,
            height_of_luminous_area_c90=None,
            height_of_luminous_area_c180=None,
            height_of_luminous_area_c270=None,
            dff_percent=None,
            lor_percent=None,
            conversion_factor=None,
            tilt=None,
            number_of_lamp_sets=None,
            lamp_sets=[],
            direct_ratios_for_room_indices=[None, None, None, None, None, None, None, None, None, None],
            c_angles=[],
            gamma_angles=[],
            intensities=[]
        )

        self.assertEqual(extracted, expected)

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
            750.
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
            header="ACME Inc.",
            type_indicator=0,
            symmetry_indicator=0,
            number_of_c_planes=1,
            distance_between_c_planes=0.0,
            number_of_intensities=37,
            distance_between_intensities=0.0,
            measurement_report="MEAS1234",
            luminaire_name="Dummy LDT file. Can be used for testing, creating screenshots, etc.",
            luminaire_number="BD0150",
            file_name="dummy.ldt",
            date_and_user="2023-05-01",
            length_of_luminaire=750.0,
            width_of_luminaire=0.0,
            height_of_luminaire=0.0,
            length_of_luminous_area=750.0,
            width_of_luminous_area=0.0,
            height_of_luminous_area_c0=10.0,
            height_of_luminous_area_c90=20.0,
            height_of_luminous_area_c180=30.0,
            height_of_luminous_area_c270=40.0,
            dff_percent=100.0,
            lor_percent=100.0,
            conversion_factor=1.0,
            tilt=0.0,
            number_of_lamp_sets=1,
            lamp_sets=[
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Generic 15W LED module",
                    total_lumens=1000.0,
                    light_color="3600K",
                    cri='90',
                    wattage=15.0
                )
            ],
            direct_ratios_for_room_indices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11],
            c_angles=[0.0],
            gamma_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2,
                400.1, 398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0,
                14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
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
            750.
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
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = LdtContent(
            header="ACME Inc.",
            type_indicator=0,
            symmetry_indicator=0,
            number_of_c_planes=1,
            distance_between_c_planes=0.0,
            number_of_intensities=37,
            distance_between_intensities=0.0,
            measurement_report="MEAS1234",
            luminaire_name="Dummy LDT file. Can be used for testing, creating screenshots, etc.",
            luminaire_number="BD0150",
            file_name="dummy.ldt",
            date_and_user="2023-05-01",
            length_of_luminaire=750.0,
            width_of_luminaire=0.0,
            height_of_luminaire=0.0,
            length_of_luminous_area=750.0,
            width_of_luminous_area=0.0,
            height_of_luminous_area_c0=10.0,
            height_of_luminous_area_c90=20.0,
            height_of_luminous_area_c180=30.0,
            height_of_luminous_area_c270=40.0,
            dff_percent=100.0,
            lor_percent=100.0,
            conversion_factor=1.0,
            tilt=0.0,
            number_of_lamp_sets=2,
            lamp_sets=[
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Set 1",
                    total_lumens=1000.0,
                    light_color="3600K",
                    cri='90',
                    wattage=20.0
                ),
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Set 2",
                    total_lumens=500.0,
                    light_color="3000K",
                    cri='80',
                    wattage=15.0
                )
            ],
            direct_ratios_for_room_indices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11],
            c_angles=[0.0],
            gamma_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            intensities=[
                2200.0, 2000.2
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
            750.
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
            header="ACME Inc.",
            type_indicator=0,
            symmetry_indicator=0,
            number_of_c_planes=1,
            distance_between_c_planes=0.0,
            number_of_intensities=37,
            distance_between_intensities=0.0,
            measurement_report="MEAS1234",
            luminaire_name="Dummy LDT file. Can be used for testing, creating screenshots, etc.",
            luminaire_number="BD0150",
            file_name="dummy.ldt",
            date_and_user="2023-05-01",
            length_of_luminaire=750.0,
            width_of_luminaire=0.0,
            height_of_luminaire=0.0,
            length_of_luminous_area=750.0,
            width_of_luminous_area=0.0,
            height_of_luminous_area_c0=10.0,
            height_of_luminous_area_c90=20.0,
            height_of_luminous_area_c180=30.0,
            height_of_luminous_area_c270=40.0,
            dff_percent=100.0,
            lor_percent=100.0,
            conversion_factor=1.0,
            tilt=0.0,
            number_of_lamp_sets=2,
            lamp_sets=[
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Set 1",
                    total_lumens=1000.0,
                    light_color="3600K",
                    cri='90',
                    wattage=20.0
                ),
                LampSet(
                    number_of_lamps=-1,
                    type_of_lamp="Set 2",
                    total_lumens=500.0,
                    light_color="3000K",
                    cri='80',
                    wattage=15.0
                )
            ],
            direct_ratios_for_room_indices=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.11],
            c_angles=[0.0],
            gamma_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5,
                65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2,
                400.1, 398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0,
                14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

if __name__ == '__main__':
    unittest.main()
