from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


class LuminaireProperties(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        for key, value in photometry.metadata.additional_properties.items():
            self.add(key.title().replace("_", " ").strip(), value)
