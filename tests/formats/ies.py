import io
import unittest
from pathlib import Path

from photometric_viewer.formats import ldt, ies
from photometric_viewer.model.luminaire import LuminousOpeningShape
from photometric_viewer.photometry.ies.converter import convert_content
from photometric_viewer.photometry.ies.extractor import extract_content

UNSUPPORTED_EXPORT_SHAPES = {
    LuminousOpeningShape.ELLIPSE_ALONG_LENGTH,
    LuminousOpeningShape.ELLIPSE_ALONG_WIDTH,
    LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH,
    LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH
}

class TestIes(unittest.TestCase):
    FILES_PATH = Path(__file__).parent / ".." / "data" / "photometrics" / "ies95"

    def test_export_ies(self):
        self.maxDiff = None
        for path in self.FILES_PATH.iterdir():
            with(self.subTest(path=path)):
                with path.open() as f:
                    content = extract_content(f)
                    photometry = convert_content(content)

                with io.StringIO() as f:
                    ies.export_to_file(f, photometry, additional_keywords={})
                    exported_value = f.getvalue()

                with io.StringIO(exported_value) as f:
                    content = extract_content(f)
                    reimported_photometry = convert_content(content)

                iesna_header = exported_value.split("\r\n")[0]
                self.assertEqual(iesna_header, "IESNA:LM-63-2002")

                photometry.metadata.file_source = ""
                reimported_photometry.metadata.file_source = ""

                # Ellipses and ellipsoids are not supported and exported as rectangles instead
                if photometry.luminous_opening_geometry.shape in UNSUPPORTED_EXPORT_SHAPES:
                    photometry.luminous_opening_geometry.shape = LuminousOpeningShape.RECTANGULAR

                self.assertEqual(photometry, reimported_photometry)

    def test_export_ldt(self):
        self.maxDiff = None
        for path in self.FILES_PATH.iterdir():
            with(self.subTest(path=path)):
                with path.open() as f:
                    content = extract_content(f)
                    luminaire = convert_content(content)

                with io.StringIO() as f:
                    ldt.export_to_file(f, luminaire)
                    exported_value = f.getvalue()

                with io.StringIO(exported_value) as f:
                    reimported_luminaire = ldt.import_from_file(f)

                self.assertEqual(luminaire.photometry.is_absolute, reimported_luminaire.photometry.is_absolute)
                self.assertEqual(luminaire.gamma_angles, reimported_luminaire.gamma_angles)
                self.assertEqual(luminaire.c_planes, reimported_luminaire.c_planes)
                self.assertEqual(luminaire.intensity_values, reimported_luminaire.intensity_values)

                self.assertEqual(luminaire.luminous_opening_geometry.width, reimported_luminaire.luminous_opening_geometry.width)
                self.assertEqual(luminaire.luminous_opening_geometry.length, reimported_luminaire.luminous_opening_geometry.length)
                self.assertEqual(luminaire.luminous_opening_geometry.height, reimported_luminaire.luminous_opening_geometry.height)

                self.assertEqual(luminaire.lamps[0].description, reimported_luminaire.lamps[0].description)

                self.assertEqual(luminaire.metadata.luminaire.replace("\n", " ")[0:78], reimported_luminaire.metadata.luminaire)
                self.assertEqual(luminaire.metadata.catalog_number, reimported_luminaire.metadata.catalog_number)


if __name__ == '__main__':
    unittest.main()
