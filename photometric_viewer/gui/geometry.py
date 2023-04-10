from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry, LuminousOpeningShape, LuminousOpening


class LuminaireGeometry(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        match photometry.luminous_opening:
            case LuminousOpening(w, l, LuminousOpeningShape.RECTANGULAR):
                self.append(self._create_item(name="Luminous opening shape", value="Rectangular"))
                self.append(self._create_item(name="Luminous opening dimensions", value=f"{w:.2f}m x {l:.2f}m"))
            case LuminousOpening(w, l, LuminousOpeningShape.ROUND):
                self.append(self._create_item(name="Luminous opening shape", value="Round"))
                self.append(self._create_item(name="Luminous opening dimensions", value=f"{w:.2f}m x {l:.2f}m"))

