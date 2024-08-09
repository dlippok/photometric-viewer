from gi.repository import Adw, Gtk
from gi.repository.Adw import ActionRow
from gi.repository.Gtk import ScrolledWindow, PolicyType, Orientation

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire


class DirectRatiosPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Direct ratios for room indices"), **kwargs)
        self.luminaire = None

        self.property_list = PropertyList()

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16
        )

        box.append(self.property_list)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.property_list.clear()

        for room_index, ratio in luminaire.metadata.direct_ratios_for_room_indices.items():
            row = ActionRow(
                title=_("Room index: {:.2f}").format(room_index),
                subtitle=f"{ratio:.3f}",
                css_classes=["property"],
                subtitle_selectable=True

            )
            self.property_list.append(row)
