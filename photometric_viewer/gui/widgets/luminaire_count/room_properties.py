from gi.repository import Gtk
from gi.repository.Adw import SpinRow
from gi.repository.Gtk import ListBox, SelectionMode

from photometric_viewer.model.room_properties import RoomProperties


class RoomPropertiesListBox(ListBox):
    def __init__(self, initial_properties: RoomProperties, on_properties_changed=None):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.on_properties_changed = on_properties_changed

        self.room_width_row = SpinRow(title=_("Room width"), value=1.5)
        self.room_width_row.connect("notify::value", self.on_update)
        self.append(self.room_width_row)

        self.room_height_row = SpinRow(title=_("Room height"), value=2)
        self.room_height_row.connect("notify::value", self.on_update)
        self.append(self.room_height_row)

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
        digits = 1
        subtitle = "Meters"
        lower = 0
        upper = 200
        step = 0.1
        page = 1

        self.room_width_row.set_digits(digits)
        self.room_width_row.set_subtitle(subtitle)
        self.room_width_row.set_adjustment(Gtk.Adjustment(
            lower=lower,
            upper=upper,
            step_increment=step,
            page_increment=page
        ))

        self.room_height_row.set_digits(digits)
        self.room_height_row.set_subtitle(subtitle)
        self.room_height_row.set_adjustment(Gtk.Adjustment(
            lower=lower,
            upper=upper,
            step_increment=step,
            page_increment=page
        ))

    def apply_values(self, room_properties: RoomProperties):
        self.room_width_row.set_value(room_properties.width)
        self.room_height_row.set_value(room_properties.height)
        self.target_illuminance.set_value(room_properties.target_illuminance)
        self.maintenance_factor.set_value(room_properties.maintenance_factor)

    def on_update(self, *args):
        room_w = self.room_width_row.get_value()
        room_h = self.room_height_row.get_value()
        illuminance = self.target_illuminance.get_value()
        mf = self.maintenance_factor.get_value()

        values = RoomProperties(
            width=room_w,
            height=room_h,
            target_illuminance=illuminance,
            maintenance_factor= mf
        )

        if self.on_properties_changed:
            self.on_properties_changed(values)
