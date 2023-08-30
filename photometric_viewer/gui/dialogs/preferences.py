import locale

from gi.repository import Adw, Gtk
from gi.repository.Gtk import ListBox, Box, Orientation, Label, SelectionMode, ToggleButton, SpinButton, Adjustment

from photometric_viewer.model.settings import Settings, DiagramStyle, SnapValueAnglesTo, DisplayHalfSpaces
from photometric_viewer.model.units import LengthUnits
from photometric_viewer.utils import plotter_themes


class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, settings: Settings, on_update_settings, **kwargs):
        super().__init__(**kwargs)
        self.page = Adw.PreferencesPage(
            title=_("Application Settings"),
        )
        self.add(self.page)

        self.set_search_enabled(False)
        self.settings = settings
        self.on_update_settings = on_update_settings
        self._add_locale_settings_group()
        self._add_curve_settings_group()

    def _add_locale_settings_group(self):
        locale_settings_group = Adw.PreferencesGroup(
            title=_("Local settings"),
            description=_("Preferred units of measurement and display settings related to your local area")
        )

        locale_settings_list = ListBox(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )
        use_units_from_file_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16
        )
        use_units_from_file_box.append(Label(label=_("Use units from photometric file"), hexpand=True, xalign=0))
        switch = Gtk.Switch(active=self.settings.length_units_from_file)
        switch.connect("state-set", self.length_units_from_file_state_set)
        use_units_from_file_box.append(switch)

        self.preferred_units_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16,
            sensitive=not self.settings.length_units_from_file
        )
        self.preferred_units_box.append(Label(label=_("Preferred length units"), hexpand=True, xalign=0))
        self.preferred_units_dropdown: Gtk.DropDown = Gtk.DropDown.new_from_strings([
            _("Meters"),
            _("Centimeters"),
            _("Millimeters"),
            _("Feet"),
            _("Inches")
        ])

        match self.settings.length_units:
            case LengthUnits.METERS:
                self.preferred_units_dropdown.set_selected(0)
            case LengthUnits.CENTIMETERS:
                self.preferred_units_dropdown.set_selected(1)
            case LengthUnits.MILLIMETERS:
                self.preferred_units_dropdown.set_selected(2)
            case LengthUnits.FEET:
                self.preferred_units_dropdown.set_selected(3)
            case LengthUnits.INCHES:
                self.preferred_units_dropdown.set_selected(4)

        self.preferred_units_dropdown.connect("notify::selected", self.preferred_unit_changed)

        self.preferred_units_box.append(self.preferred_units_dropdown)

        electricity_price_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16
        )

        electricity_price_box.append(Label(label=_("Electricity price per kWh"), hexpand=True, xalign=0))

        electricity_price_spin_button = SpinButton(
            adjustment=Adjustment(
                lower=0,
                upper=100000,
                step_increment=0.05,
                value=self.settings.electricity_price_per_kwh,
                page_size=0,
            )
        )
        electricity_price_spin_button.set_value(self.settings.electricity_price_per_kwh)
        electricity_price_spin_button.set_digits(2)
        electricity_price_spin_button.connect("value-changed", self.price_per_kwh_changed)
        electricity_price_box.append(electricity_price_spin_button)

        locale_settings_list.append(use_units_from_file_box)
        locale_settings_list.append(self.preferred_units_box)
        locale_settings_list.append(electricity_price_box)
        locale_settings_group.add(locale_settings_list)

        self.page.add(locale_settings_group)

    def _add_curve_settings_group(self):
        curve_settings_group = Adw.PreferencesGroup(
            title=_("Photometric diagram"),
            description=_("Apperance of light distribution diagram")
        )

        curve_settings_list = ListBox(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.diagram_theme_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16,
            sensitive=not self.settings.length_units_from_file
        )
        self.diagram_theme_box.append(Label(label=_("Theme"), hexpand=True, xalign=0))
        self.diagram_theme_dropdown: Gtk.DropDown = Gtk.DropDown.new_from_strings([t.name for t in plotter_themes.THEMES])
        for n, theme in enumerate(plotter_themes.THEMES):
            if theme.name == self.settings.diagram_theme:
                self.diagram_theme_dropdown.set_selected(n)
        self.diagram_theme_dropdown.connect("notify::selected", self.diagram_theme_changed)
        self.diagram_theme_box.append(self.diagram_theme_dropdown)
        curve_settings_list.append(self.diagram_theme_box)

        curve_style_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16
        )
        curve_style_buttons_box = Box(
            orientation=Orientation.HORIZONTAL,
            css_classes=["linked"]
        )

        style_simple_button = ToggleButton(
            label=_("Simple"),
            active=self.settings.diagram_style == DiagramStyle.SIMPLE
        )
        style_simple_button.connect("toggled", self.curve_style_simple_toggled)

        style_detailed_button = ToggleButton(
            label=_("Detailed"),
            group=style_simple_button,
            active=self.settings.diagram_style == DiagramStyle.DETAILED
        )
        style_detailed_button.connect("toggled", self.curve_style_detailed_toggled)

        curve_style_buttons_box.append(style_simple_button)
        curve_style_buttons_box.append(style_detailed_button)
        curve_style_box.append(Label(label=_("Style"), hexpand=True, xalign=0))
        curve_style_box.append(curve_style_buttons_box)
        curve_settings_list.append(curve_style_box)


        snap_values_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16
        )
        snap_values_buttons_box = Box(
            orientation=Orientation.HORIZONTAL,
            css_classes=["linked"]
        )

        snap_max_value_button = ToggleButton(
            label=_("Max value"),
            active=self.settings.snap_value_angles_to == SnapValueAnglesTo.MAX_VALUE
        )
        snap_max_value_button.connect("toggled", self.snap_max_value_toggled)

        snap_round_value_button = ToggleButton(
            label=_("Round number"),
            group=snap_max_value_button,
            active=self.settings.snap_value_angles_to == SnapValueAnglesTo.ROUND_NUMBER
        )
        snap_round_value_button.connect("toggled", self.snap_round_value_toggled)

        snap_values_buttons_box.append(snap_max_value_button)
        snap_values_buttons_box.append(snap_round_value_button)
        snap_values_box.append(Label(label=_("Snap guides to"), hexpand=True, xalign=0))
        snap_values_box.append(snap_values_buttons_box)
        curve_settings_list.append(snap_values_box)

        display_half_spaces_box = Box(
            orientation=Orientation.HORIZONTAL,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16
        )
        display_half_spaces_buttons_box = Box(
            orientation=Orientation.HORIZONTAL,
            css_classes=["linked"]
        )

        display_half_spaces_both_button = ToggleButton(
            label=_("Both"),
            active=self.settings.display_half_spaces == DisplayHalfSpaces.BOTH
        )
        display_half_spaces_both_button.connect("toggled", self.display_half_spaces_both_toggled)

        display_half_spaces_relevant_button = ToggleButton(
            label=_("Only relevant"),
            group=display_half_spaces_both_button,
            active=self.settings.display_half_spaces == DisplayHalfSpaces.ONLY_RELEVANT
        )
        display_half_spaces_relevant_button.connect("toggled", self.display_half_spaces_relevant_toggled)

        display_half_spaces_buttons_box.append(display_half_spaces_both_button)
        display_half_spaces_buttons_box.append(display_half_spaces_relevant_button)
        display_half_spaces_box.append(Label(label=_("Display half spaces"), hexpand=True, xalign=0))
        display_half_spaces_box.append(display_half_spaces_buttons_box)
        curve_settings_list.append(display_half_spaces_box)

        curve_settings_group.add(curve_settings_list)

        self.page.add(curve_settings_group)

    def preferred_unit_changed(self, *args):
        match self.preferred_units_dropdown.get_selected():
            case 0:
                self.settings.length_units = LengthUnits.METERS
            case 1:
                self.settings.length_units = LengthUnits.CENTIMETERS
            case 2:
                self.settings.length_units = LengthUnits.MILLIMETERS
            case 3:
                self.settings.length_units = LengthUnits.FEET
            case 4:
                self.settings.length_units = LengthUnits.INCHES
        self.update()

    def price_per_kwh_changed(self, spin_button: SpinButton, *args):
        self.settings.electricity_price_per_kwh = spin_button.get_value()
        self.update()

    def length_units_from_file_state_set(self, widget, state, *args):
        self.settings.length_units_from_file = state
        self.preferred_units_box.set_sensitive(not state)
        self.update()

    def curve_style_simple_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.diagram_style = DiagramStyle.SIMPLE
            self.update()

    def curve_style_detailed_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.diagram_style = DiagramStyle.DETAILED
            self.update()

    def snap_max_value_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.snap_value_angles_to = SnapValueAnglesTo.MAX_VALUE
            self.update()

    def snap_round_value_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.snap_value_angles_to = SnapValueAnglesTo.ROUND_NUMBER
            self.update()

    def display_half_spaces_both_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.display_half_spaces = DisplayHalfSpaces.BOTH
            self.update()

    def display_half_spaces_relevant_toggled(self, widget: ToggleButton, *args):
        if widget.get_active():
            self.settings.display_half_spaces = DisplayHalfSpaces.ONLY_RELEVANT
            self.update()

    def diagram_theme_changed(self, *args):
        selected = self.diagram_theme_dropdown.get_selected()
        self.settings.diagram_theme = plotter_themes.THEMES[selected].name
        self.update()

    def update(self):
        self.on_update_settings()
