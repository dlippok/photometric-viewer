import io
import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps, LuminousOpeningGeometry, LuminousOpeningShape
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.photometry.ies.converter import convert_content
from photometric_viewer.photometry.ies.model import IesContent, InlineAttributes, LampAttributes, MetadataTuple


class TestConvertContent(unittest.TestCase):
    def test_empty_content(self):
        content = IesContent(
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
                MetadataTuple(key='ISSUEDATE', value='2023-01-20'),
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
                photometric_factor=1.0,
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

if __name__ == '__main__':
    unittest.main()
