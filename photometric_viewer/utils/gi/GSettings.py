from typing import Callable, List

from gi.repository import Gio

from photometric_viewer.model.settings import Settings, DiagramStyle, DisplayHalfSpaces, SnapValueAnglesTo
from photometric_viewer.model.units import LengthUnits

class SettingsManager:
    SCHEMA_ID = "io.github.dlippok.photometric-viewer"

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SettingsManager, cls).__new__(cls)

            cls.instance._gsettings: Gio.Settings | None = None
            cls.instance.settings: Settings = Settings()
            cls.instance._callbacks: List[Callable[[Settings], None]] = []

            if cls.instance.SCHEMA_ID in Gio.Settings.list_schemas():
                cls.instance._gsettings: Gio.Settings = Gio.Settings.new(cls.instance.SCHEMA_ID)
                cls.instance.gsettings_available = True
            else:
                print("Could not load GSettings. Using default value")
                cls.instance.gsettings_available = False
            cls.instance.load()
        return cls.instance

    def save(self):
        if not self._gsettings:
            return

        self._gsettings.set_boolean("length-units-from-file", self.settings.length_units_from_file)
        self._gsettings.set_enum("preferred-length-units", self.settings.length_units.value)
        self._gsettings.set_double("electricity-price-per-kwh", self.settings.electricity_price_per_kwh)
        self._gsettings.set_enum("diagram-style", self.settings.diagram_style.value)
        self._gsettings.set_enum("display-half-spaces", self.settings.display_half_spaces.value)
        self._gsettings.set_enum("snap-value-angles-to", self.settings.snap_value_angles_to.value)
        self._gsettings.set_string("diagram-theme", self.settings.diagram_theme)
        self._gsettings.set_boolean("autosave", self.settings.autosave)
        self._gsettings.set_boolean("editor-word-warp", self.settings.editor_word_warp)
        self._gsettings.set_boolean("editor-grid", self.settings.editor_grid)
        self._gsettings.set_boolean("editor-highlight-current-line", self.settings.editor_highlight_current_line)
        self._gsettings.set_boolean("editor-show-line-numbers", self.settings.editor_show_line_numbers)

    def load(self):
        if self._gsettings:
            self.settings = Settings(
                length_units_from_file=self._gsettings.get_boolean("length-units-from-file"),
                length_units=LengthUnits(self._gsettings.get_enum("preferred-length-units")),
                electricity_price_per_kwh=self._gsettings.get_double("electricity-price-per-kwh"),
                diagram_style=DiagramStyle(self._gsettings.get_enum("diagram-style")),
                display_half_spaces=DisplayHalfSpaces(self._gsettings.get_enum("display-half-spaces")),
                snap_value_angles_to=SnapValueAnglesTo(self._gsettings.get_enum("snap-value-angles-to")),
                diagram_theme=self._gsettings.get_string("diagram-theme"),
                autosave=self._gsettings.get_boolean("autosave"),
                editor_word_warp=self._gsettings.get_boolean("editor-word-warp"),
                editor_grid=self._gsettings.get_boolean("editor-grid"),
                editor_highlight_current_line=self._gsettings.get_boolean("editor-highlight-current-line"),
                editor_show_line_numbers=self._gsettings.get_boolean("editor-show-line-numbers")
            )

        self.notify_update()

    def update(self):
        self.save()
        self.notify_update()

    def notify_update(self):
        for callback in self._callbacks:
            callback(self.settings)

    def register_on_update(self, callback: Callable[[Settings], None]):
        self._callbacks.append(callback)
