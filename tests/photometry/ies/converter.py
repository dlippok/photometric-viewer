import io
import unittest

from photometric_viewer.model.luminaire import Luminaire, Calculable, FileFormat, PhotometryMetadata, \
    LuminairePhotometricProperties, Lamps
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


if __name__ == '__main__':
    unittest.main()
