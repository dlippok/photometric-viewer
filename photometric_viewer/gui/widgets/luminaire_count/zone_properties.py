from gi.repository import Gtk
from gi.repository.Adw import SpinRow
from gi.repository.Gtk import ListBox, SelectionMode

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.zones import ZoneProperties
from photometric_viewer.utils.gi.GSettings import SettingsManager


class ZonePropertiesListBox(ListBox):
    LENGTH_PROPERTIES = {
    }

    def __init__(self, initial_properties: ZoneProperties, on_properties_changed=None):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.is_updating = False

        self.on_properties_changed = on_properties_changed

        self.settings_manager = SettingsManager()
        self.settings_manager.register_on_update(self.on_update_settings)
        self.settings = self.settings_manager.settings

        self.zone_width_row = SpinRow(title=_("Zone width"), value=1.5)
        self.zone_width_row.connect("notify::value", self.on_update)
        self.append(self.zone_width_row)

        self.zone_height_row = SpinRow(title=_("Zone height"), value=2)
        self.zone_height_row.connect("notify::value", self.on_update)
        self.append(self.zone_height_row)

        self.target_illuminance = SpinRow(
            title=_("Required illuminance"),
            subtitle="lx",
            adjustment=Gtk.Adjustment(
                lower=0,
                upper=1000000,
                step_increment=10,
                page_increment=100
            )

        )
        self.target_illuminance.connect("notify::value", self.on_update)
        self.append(self.target_illuminance)

        self.maintenance_factor = SpinRow(
            title=_("Maintenance factor"),
            digits=2,
            adjustment=Gtk.Adjustment(
                lower=0.01,
                upper=1,
                step_increment=0.1,
                page_increment=0.1
            )
        )
        self.maintenance_factor.connect("notify::value", self.on_update)
        self.append(self.maintenance_factor)

        self.apply_units()
        self.apply_values(initial_properties)

    def apply_units(self):
        print(f"Using units: {self.settings.length_units}")

        digits = 1
        subtitle = "Meters"
        lower = 0
        upper = 200
        step = 0.1
        page = 1

        self.zone_width_row.set_digits(digits)
        self.zone_width_row.set_subtitle(subtitle)
        self.zone_width_row.set_adjustment(Gtk.Adjustment(
            lower=lower,
            upper=upper,
            step_increment=step,
            page_increment=page
        ))

        self.zone_height_row.set_digits(digits)
        self.zone_height_row.set_subtitle(subtitle)
        self.zone_height_row.set_adjustment(Gtk.Adjustment(
            lower=lower,
            upper=upper,
            step_increment=step,
            page_increment=page
        ))

    def apply_values(self, zone_properties: ZoneProperties):
        self.zone_width_row.set_value(zone_properties.width)
        self.zone_height_row.set_value(zone_properties.height)
        self.target_illuminance.set_value(zone_properties.target_illuminance)
        self.maintenance_factor.set_value(zone_properties.maintenance_factor)

    def on_update(self, *args):
        if self.is_updating:
            return

        room_w = self.zone_width_row.get_value()
        room_h = self.zone_height_row.get_value()
        illuminance = self.target_illuminance.get_value()
        mf = self.maintenance_factor.get_value()

        values = ZoneProperties(
            width=room_w,
            height=room_h,
            target_illuminance=illuminance,
            maintenance_factor= mf
        )

        if self.on_properties_changed:
            self.on_properties_changed(values)

    def on_update_settings(self, settings: Settings):
        self.is_updating = True
        try:
            self.settings = settings
            self.apply_units()
        finally:
            self.is_updating = False
