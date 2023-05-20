from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


class GeneralLuminaireInformation(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.add_if_non_empty("Catalog Number", photometry.metadata.catalog_number)
        self.add("Manufacturer", photometry.metadata.manufacturer)
        self.add("Description", photometry.metadata.luminaire)
