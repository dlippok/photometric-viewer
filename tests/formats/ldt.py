import unittest
from pathlib import Path

from photometric_viewer.formats.ldt import import_from_file
from photometric_viewer.model.photometry import Shape, Lamps, LuminaireGeometry, LuminousOpeningGeometry
from photometric_viewer.model.units import LengthUnits


class TestLdt(unittest.TestCase):
    FILES_PATH = Path(__file__).parent / ".." / "data" / "photometrics" / "ldt"

    def test_metadata(self):
        with (self.FILES_PATH / "metadata.ldt").open() as f:
            photometry = import_from_file(f)

        self.assertEqual(photometry.lorl, 100.0)
        self.assertEqual(photometry.dff, 100)
        self.assertEqual(photometry.metadata.luminaire, "Dummy LDT file")
        self.assertEqual(photometry.metadata.manufacturer, "ACME Inc.")
        self.assertEqual(photometry.metadata.catalog_number, "BD0150")
        self.assertEqual(photometry.lamps[0].description, "LED Module")
        self.assertEqual(photometry.metadata.additional_properties["Luminaire type"],
                         "Point source with symmetry about the vertical axis")
        self.assertEqual(photometry.metadata.additional_properties["Measurement"], "TESTREP1")
        self.assertEqual(photometry.metadata.additional_properties["Filename"], "BD0150.ldt")
        self.assertEqual(photometry.metadata.additional_properties["Date and user"], "2023-05-01 Photometric Viewer")
        self.assertEqual(photometry.metadata.additional_properties["Conversion factor for luminous intensities"], 1.0)
        self.assertEqual(photometry.metadata.file_units, LengthUnits.MILLIMETERS)

    def test_relative_photometry(self):
        with (self.FILES_PATH / "relative.ldt").open() as f:
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

        self.assertFalse(photometry.is_absolute)
        self.assertEqual(photometry.c_values, expected_values)
        self.assertEqual(photometry.lamps[0].lumens_per_lamp, 250)
        self.assertEqual(photometry.lamps[0].number_of_lamps, 2)

    def test_absolute_photometry(self):
        with (self.FILES_PATH / "absolute.ldt").open() as f:
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
            (0, gamma): raw_values[i] * (expected_flux / 1000)
            for i, gamma
            in enumerate(gamma_angles)
        }

        self.assertTrue(photometry.is_absolute)
        self.assertEqual(photometry.c_values, expected_values)
        self.assertEqual(photometry.lamps[0].lumens_per_lamp, 250)
        self.assertEqual(photometry.lamps[0].number_of_lamps, 2)

    def test_no_symmetry(self):
        with (self.FILES_PATH / "no_symmetry.ldt").open() as f:
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

        c_angles = [
            0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180,
            195, 210, 225, 240, 255, 270, 285, 300, 315, 330, 345
        ]

        angle_combinations = [(c, gamma) for c in c_angles for gamma in gamma_angles]

        expected_values = {
            angle: raw_values[i % len(raw_values)] + i
            for i, angle
            in enumerate(angle_combinations)
        }

        for coord, value in expected_values.items():
            self.assertAlmostEqual(photometry.c_values[coord], value, places=5, msg=f"Invalid value for coord {coord}")

    def test_symmetry_about_vertical_axis(self):
        with (self.FILES_PATH / "symmetry_about_vertical_axis.ldt").open() as f:
            photometry = import_from_file(f)

        expected_flux = 500

        raw_values = [
            2200.0, 2000.2, 1950.0, 1700.1, 1328.4, 1115.1, 900.5, 700.4, 600.3, 501.2, 400.1,
            398.3, 380.9, 400.2, 390.5, 320.0, 185.0, 100.6, 40.1, 20.0, 15.2, 15.0, 14.0, 11.0,
            10.8, 10.8, 10.0, 7.0, 4.0, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0
        ]

        c_angles = [
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 110, 120, 130, 140, 150, 160, 170, 180,
            190, 200, 210, 220, 230, 240, 250, 260, 270,
            280, 290, 300, 310, 320, 330, 340, 350
        ]

        gamma_angles = [
            0.0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5,
            35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 52.5, 55.0, 57.5, 60.0, 62.5, 65.0,
            67.5, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5, 85.0, 87.5, 90.0
        ]

        angles = [(c, gamma) for c in c_angles for gamma in gamma_angles]

        for i, angle in enumerate(angles):
            self.assertAlmostEqual(
                photometry.c_values[angle],
                raw_values[i % len(raw_values)],
                places=5,
                msg=f"Invalid value for coord {angle}"
            )

    def test_symmetry_to_c0c180(self):
        with (self.FILES_PATH / "symmetry_to_c0c180.ldt").open() as f:
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

        c_angles = [
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 110, 120, 130, 140, 150, 160, 170, 180,
            190, 200, 210, 220, 230, 240, 250, 260, 270,
            280, 290, 300, 310, 320, 330, 340, 350
        ]

        angles = [(c, gamma) for c in c_angles for gamma in gamma_angles]

        for i, angle in enumerate(angles):
            if angle[0] < 180:
                self.assertAlmostEqual(
                    photometry.c_values[angle],
                    raw_values[i % len(raw_values)] + i,
                    places=5,
                    msg=f"Invalid directly read value for coord {angle}"
                )

                symmetry_angle = (360-angle[0], angle[1])
                self.assertAlmostEqual(
                    photometry.c_values[angle],
                    photometry.c_values[symmetry_angle],
                    places=5,
                    msg=f"Value for angle {symmetry_angle} not symmetrical to {angle})"
                )

    def test_symmetry_to_c90c270(self):
        with (self.FILES_PATH / "symmetry_to_c90c270.ldt").open() as f:
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

        c_angles = [
            0, 10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 110, 120, 130, 140, 150, 160, 170, 180,
            190, 200, 210, 220, 230, 240, 250, 260, 270,
            280, 290, 300, 310, 320, 330, 340, 350
        ]

        angles = [(c, gamma) for c in c_angles for gamma in gamma_angles]

        i = 0
        for angle in angles:
            if angle[0] < 90:
                self.assertAlmostEqual(
                    photometry.c_values[angle],
                    photometry.c_values[(180 - angle[0], angle[1])],
                    places=5,
                    msg=f"Invalid value for coord {angle}"
                )
            elif angle[0] < 270:
                self.assertAlmostEqual(
                    photometry.c_values[angle],
                    raw_values[i % len(raw_values)] + i,
                    places=5,
                    msg=f"Invalid value for coord {angle}"
                )
                i += 1
            else:
                self.assertAlmostEqual(
                    photometry.c_values[angle],
                    photometry.c_values[(270 - (270 - angle[0]), angle[1])],
                    places=5,
                    msg=f"Invalid value for coord {angle}"
                )

    def test_geometries(self):
        with (self.FILES_PATH / "rectangular_luminaire_rectangular_luminous_opening.ldt").open() as f:
            photometry = import_from_file(f)
            self.assertEqual(photometry.luminaire_geometry, LuminaireGeometry(
                length=0.12,
                width=0.06,
                height=0.03,
                shape=Shape.RECTANGULAR
            ))
            self.assertEqual(photometry.luminous_opening_geometry, LuminousOpeningGeometry(
                length=0.05,
                width=0.04,
                shape=Shape.RECTANGULAR
            ))

        with (self.FILES_PATH / "rectangular_luminaire_round_luminous_opening.ldt").open() as f:
            photometry = import_from_file(f)
            self.assertEqual(photometry.luminaire_geometry, LuminaireGeometry(
                length=0.12,
                width=0.06,
                height=0.03,
                shape=Shape.RECTANGULAR
            ))
            self.assertEqual(photometry.luminous_opening_geometry, LuminousOpeningGeometry(
                length=0.05,
                width=0.05,
                shape=Shape.ROUND
            ))

        with (self.FILES_PATH / "round_luminaire_rectangular_luminous_opening.ldt").open() as f:
            photometry = import_from_file(f)
            self.assertEqual(photometry.luminaire_geometry, LuminaireGeometry(
                length=0.12,
                width=0.12,
                height=0.03,
                shape=Shape.ROUND
            ))
            self.assertEqual(photometry.luminous_opening_geometry, LuminousOpeningGeometry(
                length=0.05,
                width=0.04,
                shape=Shape.RECTANGULAR
            ))

        with (self.FILES_PATH / "round_luminaire_round_luminous_opening.ldt").open() as f:
            photometry = import_from_file(f)
            self.assertEqual(photometry.luminaire_geometry, LuminaireGeometry(
                length=0.12,
                width=0.12,
                height=0.03,
                shape=Shape.ROUND
            ))
            self.assertEqual(photometry.luminous_opening_geometry, LuminousOpeningGeometry(
                length=0.05,
                width=0.05,
                shape=Shape.ROUND
            ))

    def test_multiple_lamp_sets(self):
        with (self.FILES_PATH / "multiple_lamp_sets.ldt").open() as f:
            photometry = import_from_file(f)

        expected_lamp_sets = [
            Lamps(
                number_of_lamps=1,
                description="Single Lamp",
                lumens_per_lamp=500.0,
                color="3000",
                cri=100,
                wattage=15.0,
                is_absolute=False
            ),
            Lamps(
                number_of_lamps=2,
                description="Double Lamp",
                lumens_per_lamp=600.0,
                color="3000",
                cri=100,
                wattage=30.0,
                is_absolute=False
            ),
            Lamps(
                number_of_lamps=1,
                description="Single Alternative Lamp",
                lumens_per_lamp=500.0,
                color="5000",
                cri=90,
                wattage=15.0,
                is_absolute=False
            )
        ]
        self.assertEqual(photometry.lamps, expected_lamp_sets)


if __name__ == '__main__':
    unittest.main()
