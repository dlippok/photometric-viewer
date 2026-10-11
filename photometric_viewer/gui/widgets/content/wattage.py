import locale

from gi.repository.Gtk import Box, Orientation, Label, Expander, Adjustment, Scale, Align, PositionType

from photometric_viewer.model.settings import Settings
from photometric_viewer.utils.calc import annual_power_consumption, energy_cost
from photometric_viewer.utils.gi.GSettings import SettingsManager


class WattageBox(Box):
    def __init__(self, wattage: float, **kwargs):
        super().__init__(
            orientation=Orientation.VERTICAL,
            homogeneous=False,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16,
            **kwargs
        )

        self.settings_manager = SettingsManager()
        self.settings_manager.register_on_update(lambda *args: self._refresh_cost_calculation())

        self.wattage: float = wattage
        self.daily_hours_of_operation = 8

        self.power_consumption_label = Label(xalign=1, selectable=True)
        self.annual_cost_label = Label(xalign=1, selectable=True)

        power_consumption_box = self.power_consumption_calculator()
        self.append(power_consumption_box)

        self._refresh_cost_calculation()

    def power_consumption_calculator(self):
        content_box = Box(
            orientation=Orientation.VERTICAL,
            margin_top=12,
            margin_start=12,
            margin_end=12
        )

        content_box.append(Label(label=_("Utilization (hours per day)"), xalign=0, yalign=0))

        daily_hours_adjustment = Adjustment(
            lower=0,
            upper=24,
            step_increment=0.5,
            value=self.daily_hours_of_operation,
            page_size=0
        )

        daily_hours_scale = Scale(hexpand=True, adjustment=daily_hours_adjustment, margin_bottom=12)
        daily_hours_scale.set_draw_value(True)
        daily_hours_scale.connect("value-changed", self._on_daily_hours_scale_value_changed)
        daily_hours_scale.add_mark(0, PositionType.BOTTOM, "0")
        daily_hours_scale.add_mark(6, PositionType.BOTTOM, "6")
        daily_hours_scale.add_mark(12, PositionType.BOTTOM, "12")
        daily_hours_scale.add_mark(18, PositionType.BOTTOM, "18")
        daily_hours_scale.add_mark(24, PositionType.BOTTOM, "24")
        content_box.append(daily_hours_scale)

        power_consumption_box = Box(orientation=Orientation.HORIZONTAL, spacing=6, homogeneous=False, halign=Align.START)
        power_consumption_box.append(Label(label=_("Annual power consumption"), xalign=0))

        power_consumption_box.append(self.power_consumption_label)
        content_box.append(power_consumption_box)

        annual_cost_box = Box(orientation=Orientation.HORIZONTAL, spacing=6, homogeneous=False, halign=Align.START)
        annual_cost_box.append(Label(label=_("Annual cost of operation"), xalign=0))

        annual_cost_box.append(self.annual_cost_label)

        content_box.append(annual_cost_box)

        return content_box

    def _on_daily_hours_scale_value_changed(self, scale: Scale, *args):
        self.daily_hours_of_operation = scale.get_value()
        self._refresh_cost_calculation()

    def _refresh_cost_calculation(self):
        power_consumption = annual_power_consumption(
            wattage=self.wattage,
            daily_hours=self.daily_hours_of_operation
        )
        self.power_consumption_label.set_label(f"{power_consumption:.1f} kWh")

        annual_cost = energy_cost(
            power_consumption_kwh=power_consumption,
            price_kwh=self.settings_manager.settings.electricity_price_per_kwh
        )

        self.annual_cost_label.set_label(locale.currency(annual_cost))
