import io
import unittest
from pathlib import Path

from photometric_viewer.formats import ldt
from photometric_viewer.formats.ies import import_from_file
from photometric_viewer.model.photometry import LuminousOpeningShape, LuminousOpeningGeometry
from photometric_viewer.model.units import LengthUnits


class TestIes(unittest.TestCase):
    FILES_PATH = Path(__file__).parent / ".." / "data" / "photometrics" / "ies"

    def test_metadata(self):
        with (self.FILES_PATH / "label_lines.ies").open() as f:
            photometry = import_from_file(f)

        self.assertEqual(photometry.metadata.luminaire, "Dummy IES file")
        self.assertEqual(photometry.metadata.manufacturer, "ACME Inc.")
        self.assertEqual(photometry.metadata.catalog_number, "BD0150")
        self.assertEqual(photometry.metadata.date_and_user, "2023-05-01")
        self.assertEqual(photometry.metadata.additional_properties["TEST"], "TESTREP1 ACME Photometrics")
        self.assertEqual(photometry.metadata.additional_properties["TESTLAB"], "ACME Photometrics")
        self.assertEqual(photometry.metadata.additional_properties["MULTILINE"],
                         "Test multiline metadata\nShould contain three lines\nDivided by LF characters")
        self.assertEqual(photometry.lamps[0].catalog_number, "LED Module")
        self.assertEqual(photometry.lamps[0].description, "Generic 15W LED module")
        self.assertEqual(photometry.lamps[0].ballast_catalog_number, "BC15345")
        self.assertEqual(photometry.lamps[0].ballast_description, "Generic")


    def test_opening_geometry_rectangular(self):
        with (self.FILES_PATH / "rectangular_opening.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.0,
            shape=LuminousOpeningShape.RECTANGULAR
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_point(self):
        with (self.FILES_PATH / "point_opening.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.0,
            length=0.0,
            height=0.0,
            shape=LuminousOpeningShape.POINT
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_rectangular_with_height(self):
        with (self.FILES_PATH / "rectangular_opening_with_height.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.56,
            shape=LuminousOpeningShape.RECTANGULAR
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_round(self):
        with (self.FILES_PATH / "round_opening.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.12,
            height=0.0,
            shape=LuminousOpeningShape.ROUND
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_round_with_height(self):
        with (self.FILES_PATH / "round_opening_with_height.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.12,
            height=0.34,
            shape=LuminousOpeningShape.ROUND
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_sphere(self):
        with (self.FILES_PATH / "sphere_opening.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.12,
            height=0.12,
            shape=LuminousOpeningShape.SPHERE
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_horizontal_cylinder_along_width(self):
        with (self.FILES_PATH / "horizontal_cylinder_opening_along_width.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.12,
            height=0.34,
            shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_ellipse_along_width(self):
        with (self.FILES_PATH / "ellipse_opening_along_width.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.56,
            shape=LuminousOpeningShape.ELLIPSE_ALONG_WIDTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_ellipse_along_length(self):
        with (self.FILES_PATH / "ellipse_opening_along_length.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.56,
            shape=LuminousOpeningShape.ELLIPSE_ALONG_LENGTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_ellipsoid_along_width(self):
        with (self.FILES_PATH / "ellipsoid_opening_along_width.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.56,
            shape=LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_ellipsoid_along_length(self):
        with (self.FILES_PATH / "ellipsoid_opening_along_length.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.34,
            height=0.56,
            shape=LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_horizontal_cylinder_along_length(self):
        with (self.FILES_PATH / "horizontal_cylinder_opening_along_length.ies").open() as f:
            photometry = import_from_file(f)

        expected_opening = LuminousOpeningGeometry(
            width=0.12,
            length=0.12,
            height=0.34,
            shape=LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH
        )

        self.assertEqual(photometry.luminous_opening_geometry, expected_opening)

    def test_opening_geometry_metric_units(self):
        with (self.FILES_PATH / "metric_units.ies").open() as f:
            photometry = import_from_file(f)

        self.assertEqual(photometry.luminous_opening_geometry.width, 0.12)
        self.assertEqual(photometry.luminous_opening_geometry.length, 0.34)
        self.assertEqual(photometry.luminous_opening_geometry.height, 0.56)
        self.assertEqual(photometry.metadata.file_units, LengthUnits.METERS)

    def test_opening_geometry_imperial_units(self):
        with (self.FILES_PATH / "imperial_units.ies").open() as f:
            photometry = import_from_file(f)
        self.assertAlmostEqual(photometry.luminous_opening_geometry.width, 0.036576, places=6)
        self.assertAlmostEqual(photometry.luminous_opening_geometry.length, 0.103632, places=6)
        self.assertAlmostEqual(photometry.luminous_opening_geometry.height, 0.170688, places=6)
        self.assertEqual(photometry.metadata.file_units, LengthUnits.FEET)

    def test_relative_photometry(self):
        with (self.FILES_PATH / "relative_photometry.ies").open() as f:
            photometry = import_from_file(f)

        expected_flux = 500

        raw_values = [
            2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2, 400.1,
            398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
            10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
        ]

        gamma_angles = [
            0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5,
            35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0,
            67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
        ]

        expected_values = {
            (0, gamma): raw_values[i] / (expected_flux / 1000)
            for i, gamma
            in enumerate(gamma_angles)
        }

        self.assertFalse(photometry.is_absolute)
        self.assertEqual(photometry.intensity_values, expected_values)
        self.assertEqual(photometry.lamps[0].lumens_per_lamp, expected_flux)

    def test_relative_photometry_with_multiplier(self):
        with (self.FILES_PATH / "relative_photometry_with_multiplier.ies").open() as f:
            photometry = import_from_file(f)

        expected_flux = 500
        multiplier = 1.5

        raw_values = [
            2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2, 400.1,
            398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
            10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
        ]

        gamma_angles = [
            0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5,
            35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0,
            67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
        ]

        expected_values = {
            (0, gamma): round(raw_values[i] / (expected_flux / 1000) * multiplier, ndigits=2)
            for i, gamma
            in enumerate(gamma_angles)
        }

        self.assertFalse(photometry.is_absolute)
        self.assertEqual(photometry.intensity_values, expected_values)
        self.assertEqual(photometry.lamps[0].lumens_per_lamp, expected_flux)

    def test_absolute_photometry(self):
        with (self.FILES_PATH / "absolute_photometry.ies").open() as f:
            photometry = import_from_file(f)

        raw_values = [
            2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2, 400.1,
            398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
            10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
        ]

        gamma_angles = [
            0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5,
            35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0,
            67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
        ]

        expected_values = {
            (0, gamma): raw_values[i]
            for i, gamma
            in enumerate(gamma_angles)
        }

        self.assertTrue(photometry.is_absolute)
        self.assertEqual(photometry.intensity_values, expected_values)
        self.assertIsNone(photometry.lamps[0].lumens_per_lamp)

    def test_absolute_photometry_with_multiplier(self):
        self.maxDiff = None

        with (self.FILES_PATH / "absolute_photometry_with_multiplier.ies").open() as f:
            photometry = import_from_file(f)

        multiplier = 1.5

        raw_values = [
            2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2, 400.1,
            398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
            10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
        ]

        gamma_angles = [
            0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5,
            35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0,
            67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
        ]

        expected_values = {
            (0, gamma): round(raw_values[i] * multiplier, ndigits=2)
            for i, gamma
            in enumerate(gamma_angles)
        }

        self.assertTrue(photometry.is_absolute)
        self.assertEqual(photometry.intensity_values, expected_values)
        self.assertIsNone(photometry.lamps[0].lumens_per_lamp)

    def test_export_ldt(self):
        self.maxDiff = None
        for path in self.FILES_PATH.iterdir():
            with(self.subTest(path=path)):
                with path.open() as f:
                    photometry = import_from_file(f)

                with io.StringIO() as f:
                    ldt.export_to_file(f, photometry)
                    exported_value = f.getvalue()

                with io.StringIO(exported_value) as f:
                    reimported_photometry = ldt.import_from_file(f)

                self.assertEqual(photometry.is_absolute, reimported_photometry.is_absolute)
                self.assertEqual(photometry.gamma_angles, reimported_photometry.gamma_angles)
                self.assertEqual(photometry.c_planes, reimported_photometry.c_planes)
                self.assertEqual(photometry.intensity_values, reimported_photometry.intensity_values)

                self.assertEqual(photometry.luminous_opening_geometry.width, reimported_photometry.luminous_opening_geometry.width)
                self.assertEqual(photometry.luminous_opening_geometry.length, reimported_photometry.luminous_opening_geometry.length)
                self.assertEqual(photometry.luminous_opening_geometry.height, reimported_photometry.luminous_opening_geometry.height)

                self.assertEqual(photometry.lamps[0].is_absolute, reimported_photometry.lamps[0].is_absolute)
                self.assertEqual(photometry.lamps[0].description, reimported_photometry.lamps[0].description)

                self.assertEqual(photometry.metadata.luminaire.replace("\n", " ")[0:78], reimported_photometry.metadata.luminaire)
                self.assertEqual(photometry.metadata.catalog_number, reimported_photometry.metadata.catalog_number)


if __name__ == '__main__':
    unittest.main()
