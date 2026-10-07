import unittest

from photometric_viewer.photometry.common import Attribute
from photometric_viewer.photometry.ldt.model import LdtContent, LampSet
from photometric_viewer.photometry.ldt.validator import validate
from photometric_viewer.photometry.validation import AttributeMissingValue, AttributeTooLong, Severity
from photometric_viewer.photometry.ldt.validation_issues import (
    LdtLampSetAttributeInvalidValue,
    LdtLampSetAttributeMissingValue,
    LdtLampSetAttributeTooLong,
    LdtLampSetNumericAttributeOutOfRange,
)


def make_content(**overrides):
    values = {
        "header": Attribute("Manufacturer", 1),
        "type_indicator": Attribute("1", 2),
        "symmetry_indicator": Attribute("0", 3),
        "number_of_c_planes": Attribute("2", 4),
        "distance_between_c_planes": Attribute("0", 5),
        "number_of_intensities": Attribute("2", 6),
        "distance_between_intensities": Attribute("0", 7),
        "measurement_report": Attribute("Report", 8),
        "luminaire_name": Attribute("Luminaire", 9),
        "luminaire_number": Attribute("123", 10),
        "file_name": Attribute("lamp.ldt", 11),
        "date_and_user": Attribute("2026-01-01", 12),
        "length_of_luminaire": Attribute("100", 13),
        "width_of_luminaire": Attribute("100", 14),
        "height_of_luminaire": Attribute("50", 15),
        "length_of_luminous_area": Attribute("90", 16),
        "width_of_luminous_area": Attribute("90", 17),
        "height_of_luminous_area_c0": Attribute("10", 18),
        "height_of_luminous_area_c90": Attribute("10", 19),
        "height_of_luminous_area_c180": Attribute("10", 20),
        "height_of_luminous_area_c270": Attribute("10", 21),
        "dff_percent": Attribute("50", 22),
        "lor_percent": Attribute("80", 23),
        "conversion_factor": Attribute("1", 24),
        "tilt": Attribute("0", 25),
        "number_of_lamp_sets": Attribute("0", 26),
        "direct_ratios_for_room_indices": [Attribute("0.5", 27 + index) for index in range(10)],
        "c_angles": [Attribute("0", 37), Attribute("180", 38)],
        "gamma_angles": [Attribute("0", 39), Attribute("180", 40)],
        "intensities": [
            Attribute("1", 41),
            Attribute("2", 42),
            Attribute("3", 43),
            Attribute("4", 44),
        ],
    }
    values.update(overrides)
    return LdtContent(**values)


class TestLdtValidator(unittest.TestCase):
    def test_valid_content_has_no_issues(self):
        self.assertEqual(validate(make_content()), [])

    def test_rejects_invalid_type_indicator(self):
        issues = validate(make_content(type_indicator=Attribute("0", 2)))
        issue = next(issue for issue in issues if issue.attribute == "type_indicator")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_invalid_symmetry_indicator(self):
        issues = validate(make_content(symmetry_indicator=Attribute("5", 3)))
        self.assertIn("symmetry_indicator", [issue.attribute for issue in issues])

    def test_rejects_percentage_above_100(self):
        issues = validate(make_content(lor_percent=Attribute("101", 23)))
        issue = next(issue for issue in issues if issue.attribute == "lor_percent")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_manufacturer_line_over_78_characters(self):
        issues = validate(make_content(header=Attribute("M" * 79, 1)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeTooLong))
        self.assertEqual(issue.attribute, "manufacturer")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_empty_text_attribute(self):
        issues = validate(make_content(measurement_report=Attribute("", 8)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeMissingValue))
        self.assertEqual(issue.attribute, "measurement_report")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_optional_attributes_are_missing_value_warnings(self):
        optional_fields = (
            ("header", "manufacturer"),
            ("type_indicator", "type_indicator"),
            ("measurement_report", "measurement_report"),
            ("luminaire_name", "luminaire_name"),
            ("luminaire_number", "luminaire_number"),
            ("file_name", "file_name"),
            ("date_and_user", "date_and_user"),
            ("length_of_luminaire", "length_of_luminaire"),
            ("width_of_luminaire", "width_of_luminaire"),
            ("height_of_luminaire", "height_of_luminaire"),
            ("length_of_luminous_area", "length_of_luminous_area"),
            ("width_of_luminous_area", "width_of_luminous_area"),
            ("height_of_luminous_area_c0", "height_of_luminous_area_c0"),
            ("height_of_luminous_area_c90", "height_of_luminous_area_c90"),
            ("height_of_luminous_area_c180", "height_of_luminous_area_c180"),
            ("height_of_luminous_area_c270", "height_of_luminous_area_c270"),
            ("dff_percent", "dff_percent"),
            ("lor_percent", "lor_percent"),
            ("conversion_factor", "conversion_factor"),
            ("tilt", "tilt"),
        )
        for content_field, issue_name in optional_fields:
            with self.subTest(attribute=issue_name):
                issues = validate(make_content(**{content_field: Attribute(None, 1)}))
                issue = next(
                    issue
                    for issue in issues
                    if isinstance(issue, AttributeMissingValue) and issue.attribute == issue_name
                )
                self.assertEqual(issue.severity, Severity.WARNING)

        for index in range(10):
            with self.subTest(attribute=f"direct_ratio_{index + 1}"):
                ratios = [Attribute("0.5", 27 + ratio_index) for ratio_index in range(10)]
                ratios[index] = Attribute(None, 27 + index)
                issues = validate(make_content(direct_ratios_for_room_indices=ratios))
                issue = next(
                    issue
                    for issue in issues
                    if isinstance(issue, AttributeMissingValue)
                    and issue.attribute == f"direct_ratio_{index + 1}"
                )
                self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_measurement_report_over_78_characters(self):
        issues = validate(make_content(measurement_report=Attribute("R" * 79, 8)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeTooLong))
        self.assertEqual(issue.attribute, "measurement_report")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_luminaire_name_over_78_characters(self):
        issues = validate(make_content(luminaire_name=Attribute("N" * 79, 9)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeTooLong))
        self.assertEqual(issue.attribute, "luminaire_name")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_luminaire_number_over_78_characters(self):
        issues = validate(make_content(luminaire_number=Attribute("L" * 79, 10)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeTooLong))
        self.assertEqual(issue.attribute, "luminaire_number")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_accepts_file_name_over_8_characters(self):
        issues = validate(make_content(file_name=Attribute("f" * 9, 11)))
        self.assertFalse(any(isinstance(issue, AttributeTooLong) and issue.attribute == "file_name" for issue in issues))

    def test_rejects_date_and_user_over_78_characters(self):
        issues = validate(make_content(date_and_user=Attribute("D" * 79, 12)))
        issue = next(issue for issue in issues if isinstance(issue, AttributeTooLong))
        self.assertEqual(issue.attribute, "date_and_user")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_lamp_type_over_24_characters(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("1", 27),
            type_of_lamp=Attribute("T" * 25, 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("4000K", 30),
            cri=Attribute("80", 31),
            wattage=Attribute("10", 32),
        )
        issues = validate(make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set]))
        issue = next(issue for issue in issues if isinstance(issue, LdtLampSetAttributeTooLong))
        self.assertEqual(issue.attribute, "type_of_lamp")
        self.assertEqual(issue.lamp_set_number, 1)
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_light_color_over_16_characters(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("1", 27),
            type_of_lamp=Attribute("LED", 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("C" * 17, 30),
            cri=Attribute("80", 31),
            wattage=Attribute("10", 32),
        )
        issues = validate(make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set]))
        issue = next(issue for issue in issues if isinstance(issue, LdtLampSetAttributeTooLong))
        self.assertEqual(issue.attribute, "light_color")
        self.assertEqual(issue.lamp_set_number, 1)
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_missing_lamp_attributes_are_warnings(self):
        lamp_fields = (
            "number_of_lamps",
            "type_of_lamp",
            "total_lumens",
            "light_color",
            "cri",
            "wattage",
        )
        for field in lamp_fields:
            with self.subTest(attribute=field):
                lamp_set = LampSet(
                    number_of_lamps=Attribute("1", 27),
                    type_of_lamp=Attribute("LED", 28),
                    total_lumens=Attribute("1000", 29),
                    light_color=Attribute("4000K", 30),
                    cri=Attribute("80", 31),
                    wattage=Attribute("10", 32),
                )
                setattr(lamp_set, field, Attribute(None, 27))
                issues = validate(
                    make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set])
                )
                issue = next(
                    issue
                    for issue in issues
                    if isinstance(issue, LdtLampSetAttributeMissingValue)
                    and issue.attribute == field
                )
                expected_severity = Severity.ERROR if field == "number_of_lamps" else Severity.WARNING
                self.assertEqual(issue.severity, expected_severity)
                self.assertEqual(issue.lamp_set_number, 1)

    def test_lamp_set_issues_include_set_number_and_attribute(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("invalid", 27),
            type_of_lamp=Attribute("LED", 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("4000K", 30),
            cri=Attribute("80", 31),
            wattage=Attribute("-2", 32),
        )
        issues = validate(
            make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set])
        )
        invalid_issue = next(
            issue for issue in issues if isinstance(issue, LdtLampSetAttributeInvalidValue)
        )
        range_issue = next(
            issue for issue in issues if isinstance(issue, LdtLampSetNumericAttributeOutOfRange)
        )
        self.assertEqual((invalid_issue.attribute, invalid_issue.lamp_set_number), ("number_of_lamps", 1))
        self.assertEqual(invalid_issue.severity, Severity.ERROR)
        self.assertEqual((range_issue.attribute, range_issue.lamp_set_number), ("wattage", 1))
        self.assertEqual(range_issue.severity, Severity.WARNING)

    def test_accepts_text_cri(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("1", 27),
            type_of_lamp=Attribute("LED", 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("4000K", 30),
            cri=Attribute(">80", 31),
            wattage=Attribute("10", 32),
        )
        issues = validate(
            make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set])
        )
        self.assertFalse(
            any(
                getattr(issue, "attribute", None) == "cri"
                and getattr(issue, "lamp_set_number", None) == 1
                for issue in issues
            )
        )

    def test_rejects_numeric_cri_above_100(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("1", 27),
            type_of_lamp=Attribute("LED", 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("4000K", 30),
            cri=Attribute("101", 31),
            wattage=Attribute("10", 32),
        )
        issues = validate(
            make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set])
        )
        issue = next(
            issue
            for issue in issues
            if isinstance(issue, LdtLampSetNumericAttributeOutOfRange)
        )
        self.assertEqual(issue.attribute, "cri")
        self.assertEqual(issue.lamp_set_number, 1)
        self.assertEqual(issue.max_value, 100)
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_numeric_cri_below_0(self):
        lamp_set = LampSet(
            number_of_lamps=Attribute("1", 27),
            type_of_lamp=Attribute("LED", 28),
            total_lumens=Attribute("1000", 29),
            light_color=Attribute("4000K", 30),
            cri=Attribute("-1", 31),
            wattage=Attribute("10", 32),
        )
        issues = validate(
            make_content(number_of_lamp_sets=Attribute("1", 26), lamp_sets=[lamp_set])
        )
        issue = next(
            issue
            for issue in issues
            if isinstance(issue, LdtLampSetNumericAttributeOutOfRange)
        )
        self.assertEqual(issue.attribute, "cri")
        self.assertEqual(issue.lamp_set_number, 1)
        self.assertEqual(issue.min_value, 0)
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_checks_declared_angle_and_intensity_counts(self):
        issues = validate(make_content(intensities=[Attribute("1", 41)]))
        self.assertIn("intensities", [issue.attribute for issue in issues])

    def test_uses_symmetry_to_check_measured_plane_count(self):
        issues = validate(
            make_content(
                symmetry_indicator=Attribute("2", 3),
                number_of_c_planes=Attribute("4", 4),
                c_angles=[Attribute(str(value), 37 + index) for index, value in enumerate((0, 90, 180, 270))],
                intensities=[Attribute(str(value), 41 + index) for index, value in enumerate(range(6))],
            )
        )
        self.assertNotIn("intensities", [issue.attribute for issue in issues])

    def test_rejects_non_numeric_percentage(self):
        issues = validate(make_content(dff_percent=Attribute("nan", 22)))
        issue = next(issue for issue in issues if issue.attribute == "dff_percent")
        self.assertEqual(issue.severity, Severity.WARNING)

    def test_rejects_angles_out_of_order(self):
        issues = validate(make_content(gamma_angles=[Attribute("10", 39), Attribute("5", 40)]))
        self.assertIn("gamma_angles", [issue.attribute for issue in issues])


if __name__ == "__main__":
    unittest.main()
