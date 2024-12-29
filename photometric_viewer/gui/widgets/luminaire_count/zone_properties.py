import dataclasses

from gi.repository import Gtk
from gi.repository.Adw import SpinRow
from gi.repository.Gtk import ListBox, SelectionMode, Adjustment

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.units import length_factor, LengthUnits
from photometric_viewer.model.zones import ZoneProperties
from photometric_viewer.utils.gi.GSettings import SettingsManager


@dataclasses.dataclass
class SpinRowProperties:
    digits: int
    lower: int
    upper: int
    step: float
    page: float
    subtitle: str

    def to_adjustment(self) -> Adjustment:
        return Gtk.Adjustment(
            lower=self.lower,
            upper=self.upper,
            step_increment=self.step,
            page_increment=self.page
        )


class ZonePropertiesListBox(ListBox):
    LENGTH_PROPERTIES = {
        LengthUnits.METERS: SpinRowProperties(
            digits=2,
            subtitle="Meters",
            lower=0,
            upper=200,
            step=0.1,
            page=1
        ),
        LengthUnits.CENTIMETERS: SpinRowProperties(
            digits=0,
            subtitle="Centimeters",
            lower=0,
            upper=20000,
            step=1,
            page=10
        ),
        LengthUnits.MILLIMETERS: SpinRowProperties(
            digits=0,
            subtitle="Millimeters",
            lower=0,
            upper=200000,
            step=1,
            page=100
        ),
        LengthUnits.FEET: SpinRowProperties(
            digits=2,
            subtitle="Feet",
            lower=0,
            upper=650,
            step=0.1,
            page=1
        ),
        LengthUnits.INCHES: SpinRowProperties(
            digits=1,
            subtitle="Inches",
            lower=0,
            upper=7800,
            step=0.1,
            page=10
        ),
    }

    def __init__(self, zone_properties: ZoneProperties, on_properties_changed=None):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.zone_properties = zone_properties
        self.is_updating = False

        self.on_properties_changed = on_properties_changed

        self.settings_manager = SettingsManager()
        self.settings_manager.register_on_update(self.on_update_settings)
        self.settings = self.settings_manager.settings

        self.zone_width_row = SpinRow(title=_("Zone width"), value=1.5)
        self.zone_width_row.connect("notify::value", self.on_update)
        self.append(self.zone_width_row)

        self.zone_length_row = SpinRow(title=_("Zone length"), value=2)
        self.zone_length_row.connect("notify::value", self.on_update)
        self.append(self.zone_length_row)

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
        self.apply_values()

    def apply_units(self):
        self.is_updating = True
        try:
            self.apply_labels()
            self.apply_values()
        finally:
            self.is_updating = False

    def apply_labels(self):
        spin_row_properties = self.LENGTH_PROPERTIES[self.settings.length_units]

        self.zone_width_row.set_digits(spin_row_properties.digits)
        self.zone_width_row.set_subtitle(_(spin_row_properties.subtitle))
        self.zone_width_row.set_adjustment(spin_row_properties.to_adjustment())

        self.zone_length_row.set_digits(spin_row_properties.digits)
        self.zone_length_row.set_subtitle(_(spin_row_properties.subtitle))
        self.zone_length_row.set_adjustment(spin_row_properties.to_adjustment())

    def apply_values(self):
        f = length_factor(self.settings.length_units)

        self.zone_width_row.set_value(self.zone_properties.width * f)
        self.zone_length_row.set_value(self.zone_properties.length * f)
        self.target_illuminance.set_value(self.zone_properties.target_illuminance)
        self.maintenance_factor.set_value(self.zone_properties.maintenance_factor)

    def on_update(self, *args):
        if self.is_updating:
            return

        f = length_factor(self.settings.length_units)

        zone_w = self.zone_width_row.get_value() / f
        zone_l = self.zone_length_row.get_value() / f
        illuminance = self.target_illuminance.get_value()
        mf = self.maintenance_factor.get_value()

        self.zone_properties.width = zone_w
        self.zone_properties.length = zone_l
        self.zone_properties.target_illuminance = illuminance
        self.zone_properties.maintenance_factor = mf

        if self.on_properties_changed:
            self.on_properties_changed()

    def on_update_settings(self, settings: Settings):
        self.settings = settings
        self.apply_units()
