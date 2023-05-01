from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, PolicyType, ScrolledWindow

from photometric_viewer.gui.geometry import LuminaireGeometry
from photometric_viewer.gui.lamps import LampAndBallast
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.gui.diagram import PhotometricDiagram
from photometric_viewer.gui.header import Header
from photometric_viewer.gui.properties import LuminaireProperties


class PhotometryContent(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagram = PhotometricDiagram()
        self.properties = LuminaireProperties()
        self.geometry = LuminaireGeometry()
        self.lamps_and_ballast = LampAndBallast()

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=32,
            margin_bottom=32,
            margin_start=32,
            margin_end=32
        )

        box.append(Header(label="Photometric diagram", xalign=0))
        box.append(self.diagram)

        box.append(Header(label="Geometry", xalign=0))
        box.append(self.geometry)

        box.append(Header(label="Lamps and ballast", xalign=0))
        box.append(self.lamps_and_ballast)

        box.append(Header(label="Properties", xalign=0))
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
        self.geometry.set_photometry(photometry)
        self.properties.set_photometry(photometry)
        self.lamps_and_ballast.set_photometry(photometry)

