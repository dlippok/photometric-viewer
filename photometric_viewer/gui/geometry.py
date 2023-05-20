from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry, Shape, LuminousOpeningGeometry, LuminaireGeometry


class LuminaireGeometryProperties(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        match photometry.luminaire_geometry:
            case LuminaireGeometry(w, l, h, Shape.RECTANGULAR):
                self.append(self._create_item(name="Luminaire shape", value="Rectangular"))
                self.append(self._create_item(name="Luminaire dimensions", value=f"{w:.2f}m x {l:.2f}m x {h:.2f}m"))
            case LuminaireGeometry(w, l, h, Shape.ROUND):
                self.append(self._create_item(name="Luminaire shape", value="Round"))
                self.append(self._create_item(name="Luminaire dimensions", value=f"{w:.2f}m x {l:.2f}m x {h:.2f}m"))

        match photometry.luminous_opening_geometry:
            case LuminousOpeningGeometry(w, l, Shape.RECTANGULAR):
                self.append(self._create_item(name="Luminous opening shape", value="Rectangular"))
                self.append(self._create_item(name="Luminous opening dimensions", value=f"{w:.2f}m x {l:.2f}m"))
            case LuminousOpeningGeometry(w, l, Shape.ROUND):
                self.append(self._create_item(name="Luminous opening shape", value="Round"))
                self.append(self._create_item(name="Luminous opening dimensions", value=f"{w:.2f}m x {l:.2f}m"))

