from gi.repository import Adw, Gdk
from gi.repository.Gtk import Box, Orientation, PolicyType, ScrolledWindow, Align

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.gui.widgets.content.diagram_highlight_details import DiagramHighlightDetails
from photometric_viewer.model.luminaire import Luminaire

from typing import Optional


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
        self.luminaire: Optional[Luminaire] = None

        self.diagram = PhotometricDiagram(show_values_under_cursor=True)
        self.diagram.set_cursor(Gdk.Cursor.new_from_name("crosshair"))
        self.diagram.highlighted_angle_changed_callback = lambda: self.highlighted_angle_changed()

        self.highlight_details = DiagramHighlightDetails()

        box.append(self.diagram)

        box.append(self.highlight_details)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.diagram.set_photometry(luminaire)

    def highlighted_angle_changed(self):
        if not self.luminaire:
            return

        if self.diagram.highlighted_angle is not None:
            candelas = {
                c_angle: self.luminaire.get_values_for_c_angle(c_angle)[self.diagram.highlighted_angle]
                for c_angle in [0, 90, 180, 270]

            }
            self.highlight_details.set_visible(True)
            self.highlight_details.update(
                gamma=self.diagram.highlighted_angle,
                values=candelas,
                locked=self.diagram.lock_angle,
                unit="cd" if self.luminaire.photometry.is_absolute else "cd/klm"
            )

        else:
            self.highlight_details.set_visible(False)

