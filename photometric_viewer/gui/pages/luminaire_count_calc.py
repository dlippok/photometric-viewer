from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, Box, ScrolledWindow, PolicyType, Label

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.luminaire_count.luminaire_count import LuminaireCountListBox
from photometric_viewer.gui.widgets.luminaire_count.room_properties import RoomPropertiesListBox
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.model.room_properties import RoomProperties
from photometric_viewer.utils import calc


class NumberOfLuminairesCalculationPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Required number of luminaires"), **kwargs)
        self.luminaire: Luminaire | None = None

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16
        )
        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        self.luminaire_count_box = LuminaireCountListBox()

        self.room_properties = self.get_default_room_properties()
        self.room_properties_box = RoomPropertiesListBox(
            initial_properties=self.room_properties,
            on_properties_changed=self.on_update_room_properties
        )
        box.append(self.room_properties_box)
        box.append(self.luminaire_count_box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def get_default_room_properties(self) -> RoomProperties:
        return RoomProperties(
            width=1.5,
            height=1.5,
            target_illuminance=500,
            maintenance_factor=0.8
        )

    def on_update_room_properties(self, room_properties):
        self.room_properties = room_properties
        self.recalculate()

    def recalculate(self):
        if not self.luminaire:
            self.luminaire_count_box.set_count(None)
            return

        photometric_properties = calc.calculate_photometry(self.luminaire)
        if not photometric_properties.luminous_flux.value:
            self.luminaire_count_box.set_count(None)
            return

        try:
            count = calc.required_number_of_luminaires(
                fulx_luminaire=photometric_properties.luminous_flux.value,
                mf=self.room_properties.maintenance_factor,
                avg_illuminance=self.room_properties.target_illuminance,
                area=self.room_properties.width * self.room_properties.height
            )
            self.luminaire_count_box.set_count(count)
        except ZeroDivisionError:
            self.luminaire_count_box.set_count(None)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.recalculate()

