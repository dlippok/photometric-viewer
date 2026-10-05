import unittest

from photometric_viewer.utils.coordinates import cartesian_to_screen


class TestCoordinatesUtils(unittest.TestCase):
    def test_cartesian_to_screen(self):
        cases = (
            ("Cartesian origin in screen origin", (0, 0), (600, 600)),
            ("Positive y values go up", (0, 1), (600, 599)),
            ("Negative y values go down", (0, -1), (600, 601)),
            ("Positive x values go to right", (1, 0), (601, 600)),
            ("Negative x values go to left", (-1, 0), (599, 600)),
        )

        for case in cases:
            with(self.subTest(case=case[0])):
                self.assertEqual(cartesian_to_screen(center=(600, 600), point=case[1]), case[2])
