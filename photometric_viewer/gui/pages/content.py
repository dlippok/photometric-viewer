from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, PolicyType, ScrolledWindow

from photometric_viewer.gui.widgets.content.general import GeneralLuminaireInformation
from photometric_viewer.gui.widgets.content.geometry import LuminaireGeometryProperties
from photometric_viewer.gui.widgets.content.lamps import LampAndBallast
from photometric_viewer.gui.widgets.content.photometry import LuminairePhotometricProperties
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.content.properties import LuminaireProperties
from photometric_viewer.model.settings import Settings


class PhotometryContent(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagram = PhotometricDiagram()
        self.general_information = GeneralLuminaireInformation()
        self.photometric_properties = LuminairePhotometricProperties()
        self.geometry = LuminaireGeometryProperties()
        self.lamps_and_ballast = LampAndBallast()
        self.properties = LuminaireProperties()

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=32,
            margin_bottom=32,
            margin_start=32,
            margin_end=32
        )

        box.append(Header(label=_("Photometric diagram"), xalign=0))
        box.append(self.diagram)

        box.append(Header(label=_("General information"), xalign=0))
        box.append(self.general_information)

        box.append(Header(label=_("Photometric properties"), xalign=0))
        box.append(self.photometric_properties)

        box.append(Header(label=_("Geometry"), xalign=0))
        box.append(self.geometry)

        box.append(Header(label=_("Lamps and ballast"), xalign=0))
        box.append(self.lamps_and_ballast)

        box.append(self.properties)

        clamp = Adw.Clamp()
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_child(scrolled_window)

    def set_photometry(self, photometry: Photometry):
        self.diagram.set_photometry(photometry)
        self.general_information.set_photometry(photometry)
        self.photometric_properties.set_photometry(photometry)
        self.geometry.set_photometry(photometry)
        self.lamps_and_ballast.set_photometry(photometry)
        self.properties.set_photometry(photometry)

    def update_settings(self, settings: Settings):
        self.diagram.update_settings(settings)
        self.geometry.update_settings(settings)
