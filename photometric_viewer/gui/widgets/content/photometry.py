from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry


def _value_with_unit(value, unit):
    if value is None:
        return None
    return f"{value}{unit}"


class LuminairePhotometricProperties(PropertyList):
    def __init__(self):
        super().__init__()

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]
        for child in items:
            self.remove(child)

        self.add(_("Light output ratio"), _value_with_unit(photometry.lorl, "%"))
        self.add(_("Downward flux fraction (DFF)"), _value_with_unit(photometry.dff, "%"))
        self.add_if_non_empty(_("Conversion factor for luminous intensities"), photometry.metadata.conversion_factor)
