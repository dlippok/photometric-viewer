from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry


class GeneralLuminaireInformation(PropertyList):
    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.add_if_non_empty(_("Catalog Number"), photometry.metadata.catalog_number)
        self.add(_("Manufacturer"), photometry.metadata.manufacturer)
        self.add(_("Description"), photometry.metadata.luminaire)
