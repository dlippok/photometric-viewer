from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.content.ldc_zoom import LdcZoom
from photometric_viewer.model.luminaire import Luminaire


class LdcZoomPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__(_("Light Distribution Curve"), **kwargs)
        self.ldc_zoom = LdcZoom()
        self.append(self.ldc_zoom)

    def set_photometry(self, luminaire: Luminaire):
        self.ldc_zoom.set_photometry(luminaire)