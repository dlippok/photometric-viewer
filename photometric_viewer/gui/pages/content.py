from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.content.header import LuminaireHeader
from photometric_viewer.gui.widgets.content.lamps import LampAndBallast
from photometric_viewer.gui.widgets.content.photometry import LuminairePhotometricProperties
from photometric_viewer.gui.widgets.content.properties import LuminaireProperties
from photometric_viewer.model.luminaire import Luminaire


class PhotometryContentPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__(_("Photometry"), **kwargs)
        self.header = LuminaireHeader()
        self.photometric_properties = LuminairePhotometricProperties()
        self.lamps_and_ballast = LampAndBallast()
        self.properties = LuminaireProperties()

        self.append(self.header)
        self.append(self.photometric_properties)
        self.append(self.lamps_and_ballast)
        self.append(self.properties)

    def set_photometry(self, luminaire: Luminaire):
        self.header.set_photometry(luminaire)
        self.photometric_properties.set_photometry(luminaire)
        self.lamps_and_ballast.set_photometry(luminaire)
        self.properties.set_photometry(luminaire)
