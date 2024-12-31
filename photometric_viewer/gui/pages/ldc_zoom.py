from gi.repository import Adw
from gi.repository.Gtk import Box, Orientation, PolicyType, ScrolledWindow, Align

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.model.luminaire import Luminaire


class LdcZoomPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Light Distribution Curve"), **kwargs)

        box = Box(
            css_classes=["card"],
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
            valign=Align.START
        )

        self.diagram = PhotometricDiagram()
        box.append(self.diagram)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.diagram.set_photometry(luminaire)