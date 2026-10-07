import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ies02.converter import convert_content
from photometric_viewer.photometry.iesna_common.model import IesContent, InlineAttributes, LampAttributes, MetadataTuple
from photometric_viewer.photometry.common import Attribute


def default_content() -> IesContent:
    return IesContent(
        header="IESNA:LM-63-2002",
        metadata=[
            MetadataTuple(key='TEST', value='TD-1234', line=1),
            MetadataTuple(key='TESTLAB', value='ACME Labs', line=1),
            MetadataTuple(key='ISSUEDATE', value='2023-01-20', line=1),
            MetadataTuple(key='MANUFAC', value='ACME Inc.', line=1),
            MetadataTuple(key='LUMCAT', value='LUM-1234', line=1),
            MetadataTuple(key='LUMINAIRE', value='Test Luminaire', line=1),
            MetadataTuple(key='LAMPCAT', value='LAMP-1234', line=1),
            MetadataTuple(key='LAMP', value='Test Lamp 30W 3000K', line=1),
            MetadataTuple(key='LAMPPOSITION', value='Test Position', line=1),
            MetadataTuple(key='BALLASTCAT', value='BALLAST-1234', line=1),
            MetadataTuple(key='BALLAST', value='Test Ballast', line=1),
            MetadataTuple(key='COLORTEMP', value='3000K', line=1),
            MetadataTuple(key='CRI', value='80', line=1)
        ],
        inline_attributes=InlineAttributes(
            number_of_lamps=Attribute("1", line=1),
            lumens_per_lamp=Attribute("-1.0", line=1),
            multiplying_factor=Attribute("1.0", line=1),
            n_v_angles=Attribute("37", line=1),
            n_h_angles=Attribute("2", line=1),
            photometry_type=Attribute("1", line=1),
            luminous_opening_units=Attribute("2", line=1),
            luminous_opening_width=Attribute("0.12", line=1),
            luminous_opening_length=Attribute("0.34", line=1),
            luminous_opening_height=Attribute("0.56", line=1),
        ),
        lamp_attributes=LampAttributes(
            ballast_factor=Attribute("1.0", line=1),
            ballast_lamp_photometric_factor=Attribute("1.0", line=1),
            input_watts=Attribute("15.0", line=1)
        ),
        v_angles=[
            Attribute("0.0", line=1),
            Attribute("2.5", line=1),
            Attribute("5.0", line=1),
            Attribute("7.5", line=1),
            Attribute("10.0", line=1),
            Attribute("12.5", line=1),
            Attribute("15.0", line=1),
            Attribute("17.5", line=1),
            Attribute("20.0", line=1),
            Attribute("22.5", line=1),
            Attribute("25.0", line=1),
            Attribute("27.5", line=1),
            Attribute("30.0", line=1),
            Attribute("32.5", line=1),
            Attribute("35.0", line=1),
            Attribute("37.5", line=1),
            Attribute("40.0", line=1),
            Attribute("42.5", line=1),
            Attribute("45.0", line=1),
            Attribute("47.5", line=1),
            Attribute("50.0", line=1),
            Attribute("52.5", line=1),
            Attribute("55.0", line=1),
            Attribute("57.5", line=1),
            Attribute("60.0", line=1),
            Attribute("62.5", line=1),
            Attribute("65.0", line=1),
            Attribute("67.5", line=1),
            Attribute("70.0", line=1),
            Attribute("72.5", line=1),
            Attribute("75.0", line=1),
            Attribute("77.5", line=1),
            Attribute("80.0", line=1),
            Attribute("82.5", line=1),
            Attribute("85.0", line=1),
            Attribute("87.5", line=1),
            Attribute("90.0", line=1)
        ],
        h_angles=[
            Attribute("0.0", line=1),
            Attribute("90.0", line=1)
        ],
        intensities=[
            Attribute("2200.0", line=1),
            Attribute("2000.2", line=1),
            Attribute("1950.0", line=1),
            Attribute("1700.1", line=1),
            Attribute("1328.4", line=1),
            Attribute("1115.1", line=1),
            Attribute("900.5", line=1),
            Attribute("700.4", line=1),
            Attribute("600.3", line=1),
            Attribute("501.2", line=1),
            Attribute("400.1", line=1),
            Attribute("398.3", line=1),
            Attribute("380.9", line=1),
            Attribute("400.2", line=1),
            Attribute("390.5", line=1),
            Attribute("320.0", line=1),
            Attribute("185.0", line=1),
            Attribute("100.6", line=1),
            Attribute("40.1", line=1),
            Attribute("20.0", line=1),
            Attribute("15.2", line=1),
            Attribute("15.0", line=1),
            Attribute("14.0", line=1),
            Attribute("11.0", line=1),
            Attribute("10.8", line=1),
            Attribute("10.8", line=1),
            Attribute("10.0", line=1),
            Attribute("7.0", line=1),
            Attribute("4.0", line=1),
            Attribute("1.2", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("1.0", line=1),
            Attribute("0.0", line=1),
            Attribute("2201.0", line=1),
            Attribute("2000.2", line=1),
            Attribute("1950.0", line=1),
            Attribute("1700.1", line=1),
            Attribute("1328.4", line=1),
            Attribute("1115.1", line=1),
            Attribute("900.5", line=1),
            Attribute("700.4", line=1),
            Attribute("600.3", line=1),
            Attribute("501.2", line=1),
            Attribute("400.1", line=1),
            Attribute("398.3", line=1),
            Attribute("380.9", line=1),
            Attribute("400.2", line=1),
            Attribute("390.5", line=1),
            Attribute("320.0", line=1),
            Attribute("185.0", line=1),
            Attribute("100.6", line=1),
            Attribute("40.1", line=1),
            Attribute("20.0", line=1),
            Attribute("15.2", line=1),
            Attribute("15.0", line=1),
            Attribute("14.0", line=1),
            Attribute("11.0", line=1),
            Attribute("10.8", line=1),
            Attribute("10.8", line=1),
            Attribute("10.0", line=1),
            Attribute("7.0", line=1),
            Attribute("4.0", line=1),
            Attribute("1.2", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("0.0", line=1),
            Attribute("1.0", line=1),
            Attribute("1.0", line=1),
        ]
    )


class TestConvertContent(unittest.TestCase):
    def test_complete_content(self):
        content = default_content()

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
                file_format=FileFormat.IES_LM63_2002,
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
                    MetadataTuple(key='PROPERTY', value='Single value', line=1),
                ],
                "expected": {
                    "PROPERTY": "Single value",
                }
            },
            {
                "title": "Multiline property with MORE",
                "given": [
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='First line', line=1),
                    MetadataTuple(key='MORE', value='Second line', line=1),
                    MetadataTuple(key='SINGLE_LINE_PROPERTY', value='Line', line=1),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='First line', line=1),
                    MetadataTuple(key='MORE', value='Second line', line=1),
                    MetadataTuple(key='MORE', value='Third line', line=1)
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
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='First line', line=1),
                    MetadataTuple(key='MULTILINE_PROPERTY1', value='Second line', line=1),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='First line', line=1),
                    MetadataTuple(key='SINGLE_LINE_PROPERTY', value='Line', line=1),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='Second line', line=1),
                    MetadataTuple(key='MULTILINE_PROPERTY2', value='Third line', line=1)
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
                content = default_content()
                content.metadata = case["given"]

                self.assertEqual(convert_content(content).metadata.additional_properties, case["expected"])

    def test_luminous_opening_calculation(self):
        test_cases = [
            {
                "title": "Point",
                "given": (0, 0, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0,
                    length=0,
                    height=0,
                    shape=LuminousOpeningShape.POINT
                )
            },
            {
                "title": "Rectangular (feet)",
                "given": (0.1, 0.2, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular (meters)",
                "given": (0.1, 0.2, 0, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {

                "title": "Rectangular with Luminous Sides (feet)",
                "given": (0.1, 0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Rectangular with Luminous Sides (meters)",
                "given": (0.1, 0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.RECTANGULAR
                ),
            },
            {
                "title": "Circular (feet)",
                "given": (-0.1, -0.1, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Circular (meters)",
                "given": (-0.1, -0.1, 0, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Ellipse (feet)",
                "given": (-0.1, -0.2, 0, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Ellipse (meters)",
                "given": (-0.1, -0.2, 0, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Vertical Cylinder (feet)",
                "given": (-0.1, -0.1, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Vertical Cylinder (meters)",
                "given": (-0.1, -0.1, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.3,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Vertical Ellipsoidal Cylinder (feet)",
                "given": (-0.1, -0.2, 0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Vertical Ellipsoidal Cylinder (meters)",
                "given": (-0.1, -0.2, 0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.ROUND
                ),
            },
            {
                "title": "Sphere (feet)",
                "given": (-0.1, -0.1, -0.1, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.1 * 0.3048,
                    height=0.1 * 0.3048,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Sphere (meters)",
                "given": (-0.1, -0.1, -0.1, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.1,
                    height=0.1,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Ellipsoidal Spheroid (feet)",
                "given": (-0.1, -0.2, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Ellipsoidal Spheroid (meters)",
                "given": (-0.1, -0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.SPHERE
                ),
            },
            {
                "title": "Horizontal Cylinder along Photometric Horizontal (feet)",
                "given": (-0.1, 0.2, -0.1, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.1 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Horizontal Cylinder along Photometric Horizontal (meters)",
                "given": (-0.1, 0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Horizontal Ellipsoidal Cylinder along Photometric Horizontal (feet)",
                "given": (-0.1, 0.2, -0.1, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.1 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Horizontal Ellipsoidal Cylinder along Photometric Horizontal (meters)",
                "given": (-0.1, 0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
                ),
            },
            {
                "title": "Horizontal Cylinder Perpendicular to Photometric Horizontal (feet)",
                "given": (0.1, -0.2, -0.2, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.2 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Horizontal Cylinder Perpendicular to Photometric Horizontal (meters)",
                "given": (0.1, -0.2, -0.2, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.2,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Horizontal Ellipsoidal Cylinder Perpendicular to Photometric Horizontal (feet)",
                "given": (0.1, -0.2, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0.2 * 0.3048,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Horizontal Ellipsoidal Cylinder Perpendicular to Photometric Horizontal (meters)",
                "given": (0.1, -0.2, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0.2,
                    height=0.3,
                    shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
                ),
            },
            {
                "title": "Vertical Circle Facing Photometric Horizontal (feet)",
                "given": (-0.1, 0, -0.1, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0,
                    height=0.1 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
                ),
            },
            {
                "title": "Vertical Circle Facing Photometric Horizontal (meters)",
                "given": (-0.1, 0, -0.1, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0,
                    height=0.1,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
                ),
            },
            {
                "title": "Vertical Ellipse Facing Photometric Horizontal (feet)",
                "given": (-0.1, 0, -0.3, 1),
                "expected": LuminousOpeningGeometry(
                    width=0.1 * 0.3048,
                    length=0,
                    height=0.3 * 0.3048,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
                ),
            },
            {
                "title": "Vertical Ellipse Facing Photometric Horizontal (meters)",
                "given": (-0.1, 0, -0.3, 2),
                "expected": LuminousOpeningGeometry(
                    width=0.1,
                    length=0,
                    height=0.3,
                    shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
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
                content = default_content()
                content.inline_attributes.luminous_opening_units = Attribute(str(case["given"][3]), line=0)
                content.inline_attributes.luminous_opening_width = Attribute(str(case["given"][0]), line=0)
                content.inline_attributes.luminous_opening_length = Attribute(str(case["given"][1]), line=0)
                content.inline_attributes.luminous_opening_height = Attribute(str(case["given"][2]), line=0)
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
                content = default_content()
                content.inline_attributes.luminous_opening_units = Attribute(str(case["given"][3]), line=0)
                content.inline_attributes.luminous_opening_width = Attribute(str(case["given"][0]), line=0)
                content.inline_attributes.luminous_opening_length = Attribute(str(case["given"][1]), line=0)
                content.inline_attributes.luminous_opening_height = Attribute(str(case["given"][2]), line=0)
                converted = convert_content(content)

                self.assertEqual(converted.metadata.file_units, case["expected"])

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
                content = default_content()
                content.inline_attributes.lumens_per_lamp = Attribute(str(case["given"]),line=1)
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
                content = default_content()
                content.inline_attributes.n_h_angles = Attribute("3",line=1)
                content.inline_attributes.n_v_angles = Attribute("1", line=1)
                content.inline_attributes.number_of_lamps = Attribute(str(case["number_of_lamps"]), line=1)
                content.inline_attributes.lumens_per_lamp = Attribute(str(case["lumens_per_lamp"]), line=1)
                content.inline_attributes.multiplying_factor = Attribute(str(case["multiplying_factor"]), line=1)
                content.lamp_attributes.ballast_factor = Attribute(str(case["ballast_factor"]), line=1)
                content.h_angles = [ Attribute("0", line=2) ]
                content.v_angles = [
                    Attribute("0", line=2),
                    Attribute("90", line=2),
                    Attribute("180", line=2)
                ]

                content.intensities=[
                    Attribute(i, line = 3)
                    for i in case["intensities"]
                ]
                self.assertEqual(convert_content(content).intensity_values, case["expected"])

if __name__ == '__main__':
    unittest.main()
