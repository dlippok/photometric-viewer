from gi.repository import Adw, Gtk
from gi.repository.Gtk import ListBox, Box, Orientation, Label, SelectionMode

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.units import LengthUnits


class PreferencesWindow(Adw.PreferencesWindow):
    def __init__(self, settings: Settings, on_update_settings, **kwargs):
        super().__init__(**kwargs)
        self.set_search_enabled(False)
        self.settings = settings
        self.on_update_settings = on_update_settings
        self._add_units_page()

    def _add_units_page(self):
        page = Adw.PreferencesPage(
            title=_("Application Settings"),
        )

        units_group = Adw.PreferencesGroup(
            title=_("Units"),
            description=_("Measurement units displayed in the application")
        )

        units_group_list = ListBox(
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

        units_group_list.append(use_units_from_file_box)
        units_group_list.append(self.preferred_units_box)
        units_group.add(units_group_list)

        page.add(units_group)
        self.add(page)

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

    def length_units_from_file_state_set(self, widget, state, *args):
        self.settings.length_units_from_file = state
        self.preferred_units_box.set_sensitive(not state)
        self.update()

    def update(self):
        self.on_update_settings()
