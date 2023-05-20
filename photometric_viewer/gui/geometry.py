from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry, Shape, LuminousOpeningGeometry, LuminaireGeometry


class LuminaireGeometryProperties(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        match photometry.luminaire_geometry:
            case LuminaireGeometry(w, l, h, Shape.RECTANGULAR):
                self.add("Luminaire shape", "Rectangular")
                self.add("Luminaire dimensions", f"{w:.2f}m x {l:.2f}m x {h:.2f}m")
            case LuminaireGeometry(w, l, h, Shape.ROUND):
                self.add("Luminaire shape", "Round")
                self.add("Luminaire dimensions", f"{w:.2f}m x {l:.2f}m x {h:.2f}m")

        match photometry.luminous_opening_geometry:
            case LuminousOpeningGeometry(w, l, Shape.RECTANGULAR):
                self.add("Luminous opening shape", "Rectangular")
                self.add("Luminous opening dimensions", f"{w:.2f}m x {l:.2f}m")
            case LuminousOpeningGeometry(w, l, Shape.ROUND):
                self.add("Luminous opening shape", "Round")
                self.add("Luminous opening dimensions", f"{w:.2f}m x {l:.2f}m")
