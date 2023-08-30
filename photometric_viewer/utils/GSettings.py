import signal

from gi.repository import Gio

from photometric_viewer.model.settings import Settings, DiagramStyle, DisplayHalfSpaces, SnapValueAnglesTo
from photometric_viewer.model.units import LengthUnits


class GSettings:
    SCHEMA_ID = "io.github.dlippok.photometric-viewer"
    settings: Gio.Settings | None = None

    def __init__(self):
        if self.SCHEMA_ID in Gio.Settings.list_schemas():
            self.settings: Gio.Settings | None = Gio.Settings.new(self.SCHEMA_ID)
        else:
            print("Could not load GSettings. Using default value")
            self.settings = None

    def save(self, settings: Settings):
        if not self.settings:
            return

        self.settings.set_boolean("length-units-from-file", settings.length_units_from_file)
        self.settings.set_enum("preferred-length-units", settings.length_units.value)
        self.settings.set_double("electricity-price-per-kwh", settings.electricity_price_per_kwh)
        self.settings.set_enum("diagram-style", settings.diagram_style.value)
        self.settings.set_enum("display-half-spaces", settings.display_half_spaces.value)
        self.settings.set_enum("snap-value-angles-to", settings.snap_value_angles_to.value)
        self.settings.set_string("diagram-theme", settings.diagram_theme)

    def load(self):
        if not self.settings:
            return Settings()

        return Settings(
            length_units_from_file=self.settings.get_boolean("length-units-from-file"),
            length_units=LengthUnits(self.settings.get_enum("preferred-length-units")),
            electricity_price_per_kwh=self.settings.get_double("electricity-price-per-kwh"),
            diagram_style=DiagramStyle(self.settings.get_enum("diagram-style")),
            display_half_spaces=DisplayHalfSpaces(self.settings.get_enum("display-half-spaces")),
            snap_value_angles_to=SnapValueAnglesTo(self.settings.get_enum("snap-value-angles-to")),
            diagram_theme=self.settings.get_string("diagram-theme")
        )