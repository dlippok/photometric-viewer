from gi.repository import Gtk
from gi.repository.Gtk import Orientation

from photometric_viewer.model.photometry import Photometry
from photometric_viewer.gui.diagram import PhotometricDiagram
from photometric_viewer.gui.header import Header
from photometric_viewer.gui.properties import LuminaireProperties


class PhotometryContent(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.diagram = PhotometricDiagram()
        self.properties = LuminaireProperties()

        self.set_orientation(Orientation.VERTICAL)
        self.set_spacing(16)
        self.set_margin_top(32)
        self.set_margin_bottom(32)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.append(Header(label="Photometric diagram", xalign=0))
        self.append(self.diagram)

        self.append(Header(label="Properties", xalign=0))
        self.append(self.properties)

    def set_photometry(self, photometry: Photometry):
        self.diagram.set_photometry(photometry)
        self.properties.set_photometry(photometry)

