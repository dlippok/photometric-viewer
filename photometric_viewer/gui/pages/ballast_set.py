from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType, Orientation

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Lamps


class BallastPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Ballast"), **kwargs)
        self.property_list = PropertyList()
        self.settings = None
        self.wattage_box = None

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

    def set_lamp_set(self, lamp_set: Lamps):
        self.property_list.clear()
        self.set_title(lamp_set.ballast_description or _('Ballast'))

        self.property_list.add_if_non_empty(_("Ballast"), lamp_set.ballast_description)
        self.property_list.add_if_non_empty(_("Ballast catalog no."), lamp_set.ballast_catalog_number)
