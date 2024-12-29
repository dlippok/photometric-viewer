from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, ScrolledWindow, PolicyType

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.luminaire_count.luminaire_count import LuminaireCountListBox
from photometric_viewer.gui.widgets.luminaire_count.zone_properties import ZonePropertiesListBox
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.model.zones import ZoneProperties
from photometric_viewer.utils import calc
from photometric_viewer.utils.calc import illuminance


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

        self.zone_properties = self.get_default_zone_properties()
        self.zone_properties_box = ZonePropertiesListBox(
            zone_properties=self.zone_properties,
            on_properties_changed=self.on_update_room_properties
        )
        box.append(self.zone_properties_box)
        box.append(self.luminaire_count_box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def get_default_zone_properties(self) -> ZoneProperties:
        return ZoneProperties(
            width=1.5,
            length=1.5,
            target_illuminance=500,
            maintenance_factor=0.8
        )

    def on_update_room_properties(self):
        self.recalculate()

    def recalculate(self):
        if not self.luminaire:
            self.luminaire_count_box.set_count(None)
            self.luminaire_count_box.set_achieved_illuminance(None)
            return

        photometric_properties = calc.calculate_photometry(self.luminaire)
        if not photometric_properties.luminous_flux.value:
            self.luminaire_count_box.set_count(None)
            self.luminaire_count_box.set_achieved_illuminance(None)
            return

        try:
            count = calc.required_number_of_luminaires(
                flux_luminaire=photometric_properties.luminous_flux.value,
                mf=self.zone_properties.maintenance_factor,
                avg_illuminance=self.zone_properties.target_illuminance,
                area=self.zone_properties.width * self.zone_properties.length
            )

            illuminance = calc.illuminance(
                flux_luminaire=photometric_properties.luminous_flux.value,
                mf=self.zone_properties.maintenance_factor,
                area=self.zone_properties.width * self.zone_properties.length
            )
            self.luminaire_count_box.set_count(count)
            self.luminaire_count_box.set_achieved_illuminance(illuminance * count)
        except ZeroDivisionError:
            self.luminaire_count_box.set_count(None)
            self.luminaire_count_box.set_achieved_illuminance(None)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.recalculate()
