from gi.repository import Gio

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.units import LengthUnits


class GSettings:
    SCHEMA_ID = "io.github.dlippok.photometrics-viewer"
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

    def load(self):
        if not self.settings:
            return Settings(length_units_from_file=False, length_units=LengthUnits.METERS)

        return Settings(
            length_units_from_file=self.settings.get_boolean("length-units-from-file"),
            length_units=LengthUnits(self.settings.get_enum("preferred-length-units"))
        )