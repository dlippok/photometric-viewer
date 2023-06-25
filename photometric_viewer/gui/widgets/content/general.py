from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry, LuminaireType


class GeneralLuminaireInformation(PropertyList):
    def __init__(self):
        super().__init__()

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.add_if_non_empty(_("Catalog Number"), photometry.metadata.catalog_number)
        self.add(_("Manufacturer"), photometry.metadata.manufacturer)
        self.add(_("Description"), photometry.metadata.luminaire)
        self.add_if_non_empty(_("Measurement"), photometry.metadata.measurement)
        self.add_if_non_empty(_("Date and user"), photometry.metadata.date_and_user)
        self.add_if_non_empty(_("Luminaire type"), self._display_liminaire_type(photometry.metadata.luminaire_type))

    @staticmethod
    def _display_liminaire_type(luminaire_type: LuminaireType | None):
        match luminaire_type:
            case LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY:
                return _("Point source with symmetry about the vertical axis")
            case LuminaireType.LINEAR:
                return _("Linear luminaire")
            case LuminaireType.POINT_SOURCE_WITH_OTHER_SYMMETRY:
                return _("Point source with any other symmetry")
            case None:
                return None

