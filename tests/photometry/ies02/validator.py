import unittest

from photometric_viewer.photometry.ies02.validation_issues import (
    Ies02HAnglesTypeCFirstValueInvalid,
    Ies02HAnglesTypeCLastValueInvalid,
    Ies02HeaderInvalid,
    Ies02IntensityValueNegative,
    Ies02IntensityValueNotNumber,
    Ies02LuminousOpeningGeometryInvalid,
    Ies02MetadataKeyMissingRequired,
    Ies02VAnglesTypeCFirstValueInvalid,
    Ies02VAnglesValueOutOfOrder,
)
from photometric_viewer.photometry.iesna_common.model import Attribute, IesContent, InlineAttributes, LampAttributes, MetadataTuple
from photometric_viewer.photometry.validation import AttributeInvalidValue, Severity
from photometric_viewer.photometry.ies02.validator import validate


class TestValidateIes02(unittest.TestCase):
    def test_intensity_values_are_numeric(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("2", 10),
                n_h_angles=Attribute("1", 11),
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            intensities=[
                Attribute("1.0", 20),
                Attribute("not-a-number", 21),
                Attribute("3.0", 22),
            ],
        )

        issues = validate(content)

        self.assertTrue(any(isinstance(issue, Ies02IntensityValueNotNumber) for issue in issues))
        self.assertTrue(any(getattr(issue, "line_number", None) == 21 for issue in issues))
        self.assertTrue(any(issue.__class__.__name__ == "Ies02NumberOfIntensitiesInvalid" for issue in issues))

    def test_intensity_count_mismatch_uses_block_line(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("2", 10),
                n_h_angles=Attribute("1", 11),
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            intensities=[
                Attribute("1.0", 20),
                Attribute("2.0", 21),
                Attribute("3.0", 22),
                Attribute("4.0", 23),
            ],
        )

        issues = validate(content)
        count_issue = next(issue for issue in issues if issue.__class__.__name__ == "Ies02NumberOfIntensitiesInvalid")
        self.assertEqual(count_issue.line_number, 22)

    def test_intensity_values_are_not_negative(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("2", 10),
                n_h_angles=Attribute("1", 11),
                photometry_type=None,
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            intensities=[
                Attribute("1.0", 20),
                Attribute("-2.0", 21),
                Attribute("3.0", 22),
            ],
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02IntensityValueNegative) for issue in issues))
        self.assertTrue(any(getattr(issue, "line_number", None) == 21 for issue in issues))

    def test_header_with_lm_63_2002_is_warning(self):
        content = IesContent(
            header="IESNA:LM:63- 2002",
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
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02HeaderInvalid) and issue.severity == Severity.WARNING for issue in issues))

    def test_missing_required_metadata_is_reported(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
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
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            metadata=[
                MetadataTuple("TEST", "A", 10),
                MetadataTuple("TESTLAB", "B", 11),
            ],
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02MetadataKeyMissingRequired) for issue in issues))

    def test_vertical_angles_must_be_ascending_for_type_a(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("4", 11),
                n_h_angles=Attribute("1", 12),
                photometry_type=Attribute("1", 10),
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            v_angles=[
                Attribute("-90", 20),
                Attribute("0", 21),
                Attribute("30", 22),
                Attribute("10", 23),
            ],
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02VAnglesValueOutOfOrder) for issue in issues))

    def test_type_c_vertical_angles_use_type_c_rule(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("2", 11),
                n_h_angles=Attribute("1", 12),
                photometry_type=Attribute("1", 10),
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            v_angles=[
                Attribute("-90", 20),
                Attribute("180", 21),
            ],
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02VAnglesTypeCFirstValueInvalid) for issue in issues))

    def test_type_c_horizontal_angles_use_type_c_rule(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=Attribute("1", 11),
                n_h_angles=Attribute("2", 12),
                photometry_type=Attribute("1", 10),
                luminous_opening_units=None,
                luminous_opening_width=None,
                luminous_opening_length=None,
                luminous_opening_height=None,
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
            h_angles=[
                Attribute("90", 20),
                Attribute("270", 21),
            ],
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02HAnglesTypeCFirstValueInvalid) for issue in issues))
        self.assertTrue(any(isinstance(issue, Ies02HAnglesTypeCLastValueInvalid) for issue in issues))

    def test_luminous_opening_geometry_is_validated(self):
        content = IesContent(
            header="IESNA:LM-63-2002",
            inline_attributes=InlineAttributes(
                number_of_lamps=None,
                lumens_per_lamp=None,
                multiplying_factor=None,
                n_v_angles=None,
                n_h_angles=None,
                photometry_type=Attribute("1", 10),
                luminous_opening_units=None,
                luminous_opening_width=Attribute("1", 20),
                luminous_opening_length=Attribute("0", 21),
                luminous_opening_height=Attribute("-1", 22),
            ),
            lamp_attributes=LampAttributes(
                ballast_factor=None,
                ballast_lamp_photometric_factor=None,
                input_watts=None,
            ),
        )

        issues = validate(content)
        self.assertTrue(any(isinstance(issue, Ies02LuminousOpeningGeometryInvalid) for issue in issues))


if __name__ == "__main__":
    unittest.main()
