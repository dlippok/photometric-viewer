from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, PolicyType, ScrolledWindow

from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.content.header import LuminaireHeader
from photometric_viewer.gui.widgets.content.lamps import LampAndBallast
from photometric_viewer.gui.widgets.content.photometry import LuminairePhotometricProperties
from photometric_viewer.gui.widgets.content.properties import LuminaireProperties
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.model.settings import Settings


class PhotometryContentPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Photometry"), **kwargs)
        self.header = LuminaireHeader()
        self.photometric_properties = LuminairePhotometricProperties()
        self.lamps_and_ballast = LampAndBallast()
        self.properties = LuminaireProperties()

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16,
        )

        box.append(self.header)
        box.append(self.photometric_properties)

        box.append(Header(label=_("Lamps and ballast"), xalign=0))
        box.append(self.lamps_and_ballast)

        box.append(self.properties)

        clamp = Adw.Clamp(maximum_size=800)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.header.set_photometry(luminaire)
        self.photometric_properties.set_photometry(luminaire)
        self.lamps_and_ballast.set_photometry(luminaire)
        self.properties.set_photometry(luminaire)

    def update_settings(self, settings: Settings):
        self.header.update_settings(settings)
