from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry


def _value_with_unit(value, unit):
    if value is None:
        return None
    return f"{value}{unit}"


class LuminairePhotometricProperties(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]
        for child in items:
            self.remove(child)

        self.add("Light output ratio", _value_with_unit(photometry.lorl, "%"))
        self.add("Downward flux fraction (DFF)", _value_with_unit(photometry.dff, "%"))
