import io
import unittest

from photometric_viewer.photometry.ies95.extractor import extract_content
from photometric_viewer.photometry.ies95.model import IesContent, InlineAttributes, LampAttributes, MetadataTuple


class TestExtractContent(unittest.TestCase):
    def test_empty_file(self):
        content = ""

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header=None,
            metadata=[],
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=None,
                n_h_angles=None,
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                photometric_factor=None,
                input_watts=None
            ),
            v_angles=[],
            h_angles=[],
            intensities=[]
        )

        self.assertEqual(extracted, expected)

    def test_header_only_file(self):
        content = "IESNA:LM-63-1995"

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[],
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=None,
                n_h_angles=None,
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                photometric_factor=None,
                input_watts=None
            ),
            v_angles=[],
            h_angles=[],
            intensities=[]
        )

        self.assertEqual(extracted, expected)

    def test_metadata_only_file(self):
        content = """
            IESNA:LM-63-1995
            [KEY] Value
            [KEY] Value 2
            [OTHER_KEY] Other Value
            [Multiple Words]
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[
                MetadataTuple("KEY", "Value"),
                MetadataTuple("KEY", "Value 2"),
                MetadataTuple("OTHER_KEY", "Other Value"),
                MetadataTuple("Multiple Words", ""),
            ],
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=None,
                n_h_angles=None,
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                photometric_factor=None,
                input_watts=None
            ),
            v_angles=[],
            h_angles=[],
            intensities=[]
        )

        self.assertEqual(extracted, expected)

    def test_tilt_only_file(self):
        content = """
            IESNA:LM-63-1995
            TILT=NONE
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[],
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=None,
                n_h_angles=None,
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                photometric_factor=None,
                input_watts=None
            ),
            v_angles=[],
            h_angles=[],
            intensities=[]
        )

        self.assertEqual(extracted, expected)

    def test_complete_file(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_missing_v_angles(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 0.0
            ],
            h_angles=[2200.0],
            intensities=[
                20.0, 15.2, 15.0, 14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_invalid_v_angles(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            Zero 2.5s 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0d
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                None, None, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, None
            ],
            h_angles=[0.0],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_missing_h_angles(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 2 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=2,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0, 2200.0],
            intensities=[
                20.0, 15.2, 15.0, 14.0, 11.0, 10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_invalid_h_angles(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            Zero
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[None],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_missing_intensities(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_invalid_intensities(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            0.0
            2200.0 a2000.2 1950a.0 1700.1a None 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0],
            intensities=[
                2200.0, None, None, None, None, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0
            ]
        )

        self.assertEqual(extracted, expected)

    def test_extra_intensities(self):
        content = """
            IESNA:LM-63-1995
            [TEST] Photometry test file
            TILT=NONE
            1 -1 1.0 37 1 1 2 -0.12 0.34 -0.56
            1.0 1.0 15
            0.0 2.5 5.0 7.5 10.0 12.5 15.0 17.5 20.0 22.5 25.0 27.5 30.0 32.5 35.0 37.5 40.0 42.5 45.0 47.5 50.0 52.5 55.0
            57.5 60.0 62.5 65.0 67.5 70.0 72.5 75.0 77.5 80.0 82.5 85.0 87.5 90.0
            0.0
            2200.0 2000.2 1950.0 1700.1 1328.4 1115.1 900.5 700.4 600.3 501.2 400.1 398.3 380.9 400.2 390.5 320.0 185.0 100.6 40.1
            20.0 15.2 15.0 14.0 11.0 10.8 10.8 10.0 7.0 4.0 1.2 0.0 0.0 0.0 0.0 0.0 1.0 0.0 1.0 1.0 1.0 1.0
        """

        f = io.StringIO(content)
        extracted = extract_content(f)

        expected = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[MetadataTuple(key='TEST', value='Photometry test file')],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=1,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=-0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=-0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                photometric_factor=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0,
                1.0, 1.0, 1.0, 1.0
            ]
        )

        self.assertEqual(extracted, expected)


if __name__ == '__main__':
    unittest.main()
