from copy import copy
from dataclasses import dataclass, field
from enum import Enum

from gi.repository import Adw, Gtk
from gi.repository.Gtk import ListBox, SelectionMode, Button, Box

from photometric_viewer.utils import plotter_themes
from photometric_viewer.utils.plotters import LightDistributionPlotterSettings, SnapValueAnglesTo, DisplayHalfSpaces, \
    DiagramStyle

MIN_LDC_SIZE = 50
MAX_LDC_SIZE = 10000


class LdcExportFileType(Enum):
    PNG = 0
    SVG = 1


class ThemeVariant(Enum):
    BRIGHT = 0
    DARK = 1


class Background(Enum):
    SOLID = 0
    TRANSPARENT = 1


class SnapValuesTo(Enum):
    MAX_VALUE = 0
    ROUND_NUMBER = 1


@dataclass
class LdcExportFileProperties:
    size_in_px: int = 300
    file_type: LdcExportFileType = LdcExportFileType.PNG
    plotter_settings: LightDistributionPlotterSettings = field(
        default_factory=lambda: LightDistributionPlotterSettings()
    )


class LdcExportFilePropertiesBox(ListBox):
    def __init__(self, on_properties_changed=None, on_export_clicked=None):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.properties = LdcExportFileProperties()
        self.on_properties_changed = on_properties_changed
        self.on_export_clicked = on_export_clicked

        self.file_size_row = Adw.EntryRow(
            title=_("Size in px"),
            text=str(self.properties.size_in_px),
            input_purpose=Gtk.InputPurpose.DIGITS,
        )
        self.file_size_row.connect("notify::text", lambda *args: self.update())
        self.append(self.file_size_row)

        self.file_type_row = Adw.ComboRow(
            title=_("File type"),
            model=Gtk.StringList.new(["PNG", "SVG"])
        )
        self.file_type_row.connect("notify::selected", lambda *args: self.update())
        self.append(self.file_type_row)

        self.curve_background = Adw.ComboRow(
                title=_("Background"),
                model=Gtk.StringList.new([
                    _("Solid"),
                    _("Transparent")
                ])
        )
        self.curve_background.connect("notify::selected", lambda *args: self.update())
        self.append(self.curve_background)

        expander_row = Adw.ExpanderRow(
            title=_("Curve Appearance"),
        )
        self.append(expander_row)

        self.diagram_style = Adw.ComboRow(
            title=_("Style"),
            model=Gtk.StringList.new([
                _("Simple"),
                _("Detailed")
            ])
        )
        self.diagram_style.connect("notify::selected", lambda *args: self.update())
        expander_row.add_row(self.diagram_style)


        self.curve_theme_row = Adw.ComboRow(
                title=_("Theme"),
                model=Gtk.StringList.new([theme.name for theme in plotter_themes.THEMES])
        )
        self.curve_theme_row.connect("notify::selected", lambda *args: self.update())
        expander_row.add_row(self.curve_theme_row)

        self.curve_theme_variant = Adw.ComboRow(
                title=_("Variant"),
                model=Gtk.StringList.new([
                    _("Bright"),
                    _("Dark")
                ])
        )
        self.curve_theme_variant.connect("notify::selected", lambda *args: self.update())
        expander_row.add_row(self.curve_theme_variant)

        self.snap_values_row = Adw.ComboRow(
                title=_("Snap guides to"),
                model=Gtk.StringList.new([
                    _("Max value"),
                    _("Round number")
                ])
        )
        self.snap_values_row.connect("notify::selected", lambda *args: self.update())
        expander_row.add_row(self.snap_values_row)

        self.display_half_spaces = Adw.ComboRow(
            title=_("Display half spaces"),
            model=Gtk.StringList.new([
                _("Both"),
                _("Only relevant")
            ])
        )
        self.display_half_spaces.connect("notify::selected", lambda *args: self.update())
        expander_row.add_row(self.display_half_spaces)

        self.export_button = Button(label=_("Export"))
        self.export_button.connect("clicked", lambda *args: self.on_export_clicked())
        export_box = Box(
            orientation=Gtk.Orientation.HORIZONTAL,
            spacing=16,
            margin_top=4,
            margin_bottom=4,
            margin_end=4,
            hexpand=True,
            halign=Gtk.Align.END
        )

        export_box.append(self.export_button)
        self.append(export_box)

    def validate(self):
        valid = True

        file_size = self.file_size_row.get_text()
        if not file_size.isdigit() or int(file_size) < MIN_LDC_SIZE or int(file_size) > MAX_LDC_SIZE:
            self.file_size_row.set_state_flags(Gtk.StateFlags.INCONSISTENT, True)
            self.export_button.set_sensitive(False)
            self.file_size_row.set_css_classes(["error"])
            valid = False
        else:
            self.file_size_row.set_css_classes([])

        self.export_button.set_sensitive(valid)
        return valid

    def update(self):
        is_valid = self.validate()

        if not is_valid:
            return

        self.properties.size_in_px = int(self.file_size_row.get_text())
        self.properties.file_type = LdcExportFileType(self.file_type_row.get_selected())

        self._update_theme()

        if self.on_properties_changed:
            self.on_properties_changed(self.properties)

    def _update_theme(self):
        theme_variant = ThemeVariant(self.curve_theme_variant.get_selected())

        selected_theme = plotter_themes.THEMES[self.curve_theme_row.get_selected()]
        theme_by_variant = {
            ThemeVariant.BRIGHT: selected_theme.plotter_theme,
            ThemeVariant.DARK: selected_theme.plotter_theme_dark
        }

        background = Background(self.curve_background.get_selected())
        self.properties.plotter_settings.theme = theme_by_variant[theme_variant]

        new_theme = copy(self.properties.plotter_settings.theme)
        if background == Background.TRANSPARENT:
            new_theme.background_color = None
        else:
            backgrounds_by_theme = {
                ThemeVariant.BRIGHT: (1, 1, 1, 1),
                ThemeVariant.DARK: (0, 0, 0, 1)
            }
            background_color = backgrounds_by_theme[theme_variant]
            new_theme.background_color = new_theme.background_color or background_color

        self.properties.plotter_settings.theme = new_theme
        self.properties.plotter_settings.snap_value_angles_to = SnapValueAnglesTo(self.snap_values_row.get_selected() + 1)
        self.properties.plotter_settings.display_half_spaces = DisplayHalfSpaces(self.display_half_spaces.get_selected() + 1)
        self.properties.plotter_settings.style = DiagramStyle(self.diagram_style.get_selected() + 1)
