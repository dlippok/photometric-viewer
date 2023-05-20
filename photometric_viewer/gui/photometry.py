from photometric_viewer.gui.widgets.common import PropertyList
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

        self.append(self._create_item(name="Light output ratio", value=_value_with_unit(photometry.lorl, "%")))
        self.append(self._create_item(name="Downward flux fraction (DFF)", value=_value_with_unit(photometry.dff, "%")))
