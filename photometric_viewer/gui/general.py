from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


class GeneralLuminaireInformation(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.append(self._create_item(name="Name", value=photometry.metadata.luminaire))
        self.append(self._create_item(name="Manufacturer", value=photometry.metadata.manufacturer))

