from gi.repository import Gtk
from gi.repository.Gtk import Align
from gi.repository.Gtk import Orientation

from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.model.luminaire import Luminaire


class LdcZoom(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["card"],
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16,
            valign=Align.START
        )

        self.diagram = PhotometricDiagram()
        self.append(self.diagram)

    def set_photometry(self, luminaire: Luminaire):
        self.diagram.set_photometry(luminaire)