from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


class LuminaireProperties(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.append(self._create_item(name="Name", value=photometry.metadata.luminaire))
        self.append(self._create_item(name="Manufacturer", value=photometry.metadata.manufacturer))

        for key, value in photometry.metadata.additional_properties.items():
            self.append(self._create_item(name=key, value=value))
