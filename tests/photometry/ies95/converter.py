import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ies95.converter import convert_content
from photometric_viewer.photometry.ies95.model import IesContent, InlineAttributes, LampAttributes, MetadataTuple


class TestConvertContent(unittest.TestCase):
    def test_empty_content(self):
        content = IesContent()

        expected = Luminaire(
            gamma_angles=[],
            c_planes=[],
            intensity_values={},
            luminous_opening_geometry=None,
            geometry=None,
            lamps=[
                Lamps(
                    number_of_lamps=None,
                    description=None,
                    catalog_number=None,
                    position=None,
                    lumens_per_lamp=None,
                    wattage=None,
                    color=None,
                    cri=None,
                    ballast_description=None,
                    ballast_catalog_number=None
                )
            ],
            metadata=PhotometryMetadata(
                catalog_number=None,
                luminaire=None,
                manufacturer=None,
                date_and_user=None,
                additional_properties={},
                file_source="",
                file_format=FileFormat.IES,
                file_units=LengthUnits.METERS
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

    def test_complete_content(self):
        content = IesContent(
            header="IESNA:LM-63-1995",
            metadata=[
                MetadataTuple(key='TEST', value='TD-1234'),
                MetadataTuple(key='TESTLAB', value='ACME Labs'),
                MetadataTuple(key='DATE', value='2023-01-20'),
                MetadataTuple(key='MANUFAC', value='ACME Inc.'),
                MetadataTuple(key='LUMCAT', value='LUM-1234'),
                MetadataTuple(key='LUMINAIRE', value='Test Luminaire'),
                MetadataTuple(key='LAMPCAT', value='LAMP-1234'),
                MetadataTuple(key='LAMP', value='Test Lamp 30W 3000K'),
                MetadataTuple(key='LAMPPOSITION', value='Test Position'),
                MetadataTuple(key='BALLASTCAT', value='BALLAST-1234'),
                MetadataTuple(key='BALLAST', value='Test Ballast'),
                MetadataTuple(key='COLORTEMP', value='3000K'),
                MetadataTuple(key='CRI', value='80')
            ],
            inline_attributes=InlineAttributes(
                number_of_lamps=1,
                lumens_per_lamp=-1.0,
                multiplying_factor=1.0,
                n_v_angles=37,
                n_h_angles=2,
                photometry_type=1,
                luminous_opening_units=2,
                luminous_opening_width=0.12,
                luminous_opening_length=0.34,
                luminous_opening_height=0.56,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=1.0,
                future_use=1.0,
                input_watts=15.0
            ),
            v_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            h_angles=[0.0, 90.0],
            intensities=[
                2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 0.0,
                2201.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5,
                700.4, 600.3, 501.2, 400.1, 398.3, 380.9, 400.2, 390.5,
                320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
                10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0,
                1.0, 1.0,

            ]
        )

        expected = Luminaire(
            gamma_angles=[
                0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0,
                32.5, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0,
                62.5, 65.0, 67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
            ],
            c_planes=[0.0, 90.0],
            intensity_values={
                (0.0, 0.0): 2200.0, (0.0, 2.5): 2000.2, (0.0, 5.0): 1950.0, (0.0, 7.5): 1700.1,
                (0.0, 10.0): 1328.4, (0.0, 12.5): 1115.1, (0.0, 15.0): 900.5, (0.0, 17.5): 700.4,
                (0.0, 20.0): 600.3, (0.0, 22.5): 501.2, (0.0, 25.0): 400.1, (0.0, 27.5): 398.3,
                (0.0, 30.0): 380.9, (0.0, 32.5): 400.2, (0.0, 35.0): 390.5, (0.0, 37.5): 320.0,
                (0.0, 40.0): 185.0, (0.0, 42.5): 100.6, (0.0, 45.0): 40.1, (0.0, 47.5): 20.0,
                (0.0, 50.0): 15.2, (0.0, 52.5): 15.0, (0.0, 55.0): 14.0, (0.0, 57.5): 11.0,
                (0.0, 60.0): 10.8, (0.0, 62.5): 10.8, (0.0, 65.0): 10.0, (0.0, 67.5): 7.0,
                (0.0, 70.0): 4.0, (0.0, 72.5): 1.2, (0.0, 75.0): 0.0, (0.0, 77.5): 0.0,
                (0.0, 80.0): 0.0, (0.0, 82.5): 0.0, (0.0, 85.0): 0.0, (0.0, 87.5): 1.0,
                (0.0, 90.0): 0.0,
                (90.0, 0.0): 2201.0, (90.0, 2.5): 2000.2, (90.0, 5.0): 1950.0, (90.0, 7.5): 1700.1,
                (90.0, 10.0): 1328.4, (90.0, 12.5): 1115.1, (90.0, 15.0): 900.5, (90.0, 17.5): 700.4,
                (90.0, 20.0): 600.3, (90.0, 22.5): 501.2, (90.0, 25.0): 400.1, (90.0, 27.5): 398.3,
                (90.0, 30.0): 380.9, (90.0, 32.5): 400.2, (90.0, 35.0): 390.5, (90.0, 37.5): 320.0,
                (90.0, 40.0): 185.0, (90.0, 42.5): 100.6, (90.0, 45.0): 40.1, (90.0, 47.5): 20.0,
                (90.0, 50.0): 15.2, (90.0, 52.5): 15.0, (90.0, 55.0): 14.0, (90.0, 57.5): 11.0,
                (90.0, 60.0): 10.8, (90.0, 62.5): 10.8, (90.0, 65.0): 10.0, (90.0, 67.5): 7.0,
                (90.0, 70.0): 4.0, (90.0, 72.5): 1.2, (90.0, 75.0): 0.0, (90.0, 77.5): 0.0,
                (90.0, 80.0): 0.0, (90.0, 82.5): 0.0, (90.0, 85.0): 0.0, (90.0, 87.5): 1.0,
                (90.0, 90.0): 1.0,
            },
            luminous_opening_geometry=LuminousOpeningGeometry(
                width=0.12,
                length=0.34,
                height=0.56,
                shape=LuminousOpeningShape.RECTANGULAR
            ),
            geometry=None,
            lamps=[
                Lamps(
                    number_of_lamps=1,
                    description="Test Lamp 30W 3000K",
                    catalog_number="LAMP-1234",
                    position="Test Position",
                    lumens_per_lamp=None,
                    wattage=15.0,
                    color="3000K",
                    cri="80",
                    ballast_description="Test Ballast",
                    ballast_catalog_number="BALLAST-1234"
                )
            ],
            metadata=PhotometryMetadata(
                catalog_number="LUM-1234",
                luminaire="Test Luminaire",
                manufacturer="ACME Inc.",
                date_and_user="2023-01-20",
                additional_properties={
                    "TEST": "TD-1234",
                    "TESTLAB": "ACME Labs"
                },
                file_source="",
                file_format=FileFormat.IES,
                file_units=LengthUnits.METERS
            ),
            photometry=LuminairePhotometricProperties(
                is_absolute=True,
                luminous_flux=Calculable(None),
                lor=Calculable(None),
                dff=Calculable(None),
                efficacy=Calculable(None)
            )
        )

        self.assertEqual(convert_content(content), expected)

    def test_additional_property_parsing(self):
        test_cases = [
            {
                "title": "Single property",
                "given": [
                    MetadataTuple(key='PROPERTY', value='Single value'),
                ],
                "expected": {
                    "PROPERTY": "Single value",
                }
            },
            {
                "title": "Multiline property with MORE",
                "given": [
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='First line'),
                    MetadataTuple(key='MORE', value='Second line'),
                    MetadataTuple(key='SINGLE_LINE_PROPERTY', value='Line'),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='First line'),
                    MetadataTuple(key='MORE', value='Second line'),
                    MetadataTuple(key='MORE', value='Third line')
                ],
                "expected": {
                    "MULTILINE_PROPERTY1": "First line\nSecond line",
                    "SINGLE_LINE_PROPERTY": "Line",
                    "MULTILINE_PROPERTY2": "First line\nSecond line\nThird line"
                }
            },
            {
                "title": "Multiline property with repeated keyword",
                "given": [
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='First line'),
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='Second line'),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='First line'),
                    MetadataTuple(key='SINGLE_LINE_PROPERTY', value='Line'),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='Second line'),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='Third line')
                ],
                "expected": {
                    "MULTILINE_PROPERTY1": "First line\nSecond line",
                    "SINGLE_LINE_PROPERTY": "Line",
                    "MULTILINE_PROPERTY2": "First line\nSecond line\nThird line"
                }
            },

        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = IesContent(
                    metadata=case["given"]
                )

                self.assertEqual(convert_content(content).metadata.additional_properties, case["expected"])

    def test_luminous_opening_calculation(self):
        test_cases = [
            {
                "title": "Point source",
                "given": (0, 0, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0,
                    length=0,
                    height=0,
                    shape=LuminousOpeningShape.POINT
                )
            },
            {
                "title": "Rectangular opening in feet",
                "given": (0.1, 0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in meters",
                "given": (0.1, 0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in feet without height",
                "given": (0.1, 0.2, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in meters without height",
                "given": (0.1, 0.2, 0, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in feet without width",
                "given": (0, 0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.2 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in meters without width",
                "given": (0, 0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.2,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in feet without length",
                "given": (0.1, 0, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular opening in meters without length",
                "given": (0.1, 0, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.3,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Round opening in feet",
                "given": (-0.1, -0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in meters without length",
                "given": (-0.1, -0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in feet without height",
                "given": (-0.1, -0.2, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in meters without height",
                "given": (-0.1, -0.2, 0, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in feet without width",
                "given": (0, -0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.2 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in meters without width",
                "given": (0, -0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.2,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in feet without length",
                "given": (-0.1, 0, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Round opening in meters without length",
                "given": (-0.1, 0, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.3,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Sphere opening in feet",
                "given": (-0.1, 0, -0.1, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.1 * 0.3048,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Sphere opening in meters",
                "given": (-0.1, 0, -0.1, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.1,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Horizontal cylinder along length opening in feet",
                "given": (0, 0.2, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.2 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Horizontal cylinder along length opening in meters",
                "given": (0, 0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.2,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Horizontal cylinder along width opening in feet",
                "given": (0.1, 0, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Horizontal cylinder along width opening in meters",
                "given": (0.1, 0, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.3,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Ellipse along length opening in feet",
                "given": (-0.1, 0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
                ),
            },
            {
                "title": "Ellipse along length opening in meters",
                "given": (-0.1, 0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
                ),
            },
            {
                "title": "Ellipse along width opening in feet",
                "given": (0.1, -0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_WIDTH
                ),
            },
            {
                "title": "Ellipse along width opening in meters",
                "given": (0.1, -0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_WIDTH
                ),
            },
            {
                "title": "Ellipsoid along length opening in feet",
                "given": (-0.1, 0.2, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH
                ),
            },
            {
                "title": "Ellipsoid along length opening in meters",
                "given": (-0.1, 0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH
                ),
            },
            {
                "title": "Ellipsoid along width opening in feet",
                "given": (0.1, -0.2, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH
                ),
            },
            {
                "title": "Ellipsoid along width opening in meters",
                "given": (0.1, -0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH
                ),
            },
            {
                "title": "None width",
                "given": (None, 0.2, 0.3, 2),
                "expected": None
            },
            {
                "title": "None length",
                "given": (0.1, None, 0.3, 2),
                "expected": None
            },
            {
                "title": "None height",
                "given": (0.1, 0.2, None, 2),
                "expected": None
            },
            {
                "title": "All None except units",
                "given": (None, None, None, 2),
                "expected": None
            },
            {
                "title": "All None",
                "given": (None, None, None, None),
                "expected": None
            }
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = IesContent(
                    header="IESNA:LM-63-1995",
                    inline_attributes=InlineAttributes(
                        luminous_opening_units=case["given"][3],
                        luminous_opening_width=case["given"][0],
                        luminous_opening_length=case["given"][1],
                        luminous_opening_height=case["given"][2],
                    )
                )

                converted = convert_content(content)

                self.assertEqual(converted.luminous_opening_geometry, case["expected"])

    def test_file_units(self):
        test_cases = [
            {
                "title": "Size in feet",
                "given": (0.1, 0.2, 0.3, 1),
                "expected":  LengthUnits.FEET
            },
            {
                "title": "Size in meters",
                "given": (0.1, 0.2, 0.3, 2),
                "expected":  LengthUnits.METERS
            }
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = IesContent(
                    inline_attributes=InlineAttributes(
                        luminous_opening_units=case["given"][3],
                        luminous_opening_width=case["given"][0],
                        luminous_opening_length=case["given"][1],
                        luminous_opening_height=case["given"][2],
                    )
                )

                converted = convert_content(content)

                self.assertAlmostEqual(converted.metadata.file_units, case["expected"])

    def test_detect_absolute_photometry(self):
        test_cases = [
            {
                "title": "Absolute photometry",
                "given": -1,
                "expected": True
            },
            {
                "title": "Relative photometry",
                "given": 600,
                "expected": False
            }
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = IesContent(
                    inline_attributes=InlineAttributes(
                        lumens_per_lamp=case["given"]
                    )
                )
                self.assertEqual(convert_content(content).photometry.is_absolute, case["expected"])

    def test_calculating_intensities(self):
        test_cases = [
            {
                "title": "Absolute photometry",
                "number_of_lamps": 1,
                "lumens_per_lamp": -1,
                "multiplying_factor": 1,
                "ballast_factor": 1,
                "intensities": [1, 2, 3],
                "expected": {
                    (0, 0): 1,
                    (0, 90): 2,
                    (0, 180): 3
                }
            },
            {
                "title": "Relative photometry 500 lm",
                "number_of_lamps": 1,
                "lumens_per_lamp": 500,
                "multiplying_factor": 1,
                "ballast_factor": 1,
                "intensities": [1, 2, 3],
                "expected": {
                    (0, 0): 2,
                    (0, 90): 4,
                    (0, 180): 6
                }
            },
            {
                "title": "Relative photometry 500 lm, no factors",
                "number_of_lamps": 1,
                "lumens_per_lamp": 500,
                "multiplying_factor": None,
                "ballast_factor": None,
                "intensities": [1, 2, 3],
                "expected": {
                    (0, 0): 2,
                    (0, 90): 4,
                    (0, 180): 6
                }
            },
            {
                "title": "Relative photometry 500 lm, applied multiplying factor",
                "number_of_lamps": 1,
                "lumens_per_lamp": 500,
                "multiplying_factor": 2,
                "ballast_factor": 1.0,
                "intensities": [1, 2, 3],
                "expected": {
                    (0, 0): 4,
                    (0, 90): 8,
                    (0, 180): 12
                }
            },
            {
                "title": "Relative photometry 500 lm, applied ballast factor",
                "number_of_lamps": 1,
                "lumens_per_lamp": 500,
                "multiplying_factor": 1.0,
                "ballast_factor": 2,
                "intensities": [1, 2, 3],
                "expected": {
                    (0, 0): 4,
                    (0, 90): 8,
                    (0, 180): 12
                }
            },
        ]

        for case in test_cases:
            with self.subTest(title=case["title"]):
                content = IesContent(
                    inline_attributes=InlineAttributes(
                        n_h_angles=3,
                        n_v_angles=1,
                        number_of_lamps=case["number_of_lamps"],
                        lumens_per_lamp=case["lumens_per_lamp"],
                        multiplying_factor=case["multiplying_factor"],
                    ),
                    h_angles=[0],
                    v_angles=[0, 90, 180],
                    lamp_attributes=LampAttributes(
                        ballast_factor=case["ballast_factor"]
                    ),
                    intensities=case["intensities"]
                )
                self.assertEqual(convert_content(content).intensity_values, case["expected"])


if __name__ == '__main__':
    unittest.main()
