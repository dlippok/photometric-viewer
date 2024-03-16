from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.Gtk import Box, Orientation

from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils import calc


def _value_with_unit(value, unit):
    if value is None:
        return None
    return f"{value}{unit}"


class LuminairePhotometricProperties(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.VERTICAL,
            spacing=16
        )

        self.property_list = PropertyList()
        self.append(Header(label=_("Photometric properties"), xalign=0))
        self.append(self.property_list)

    def set_photometry(self, luminaire: Luminaire):
        self.property_list.clear()
        photometric_properties = calc.calculate_photometry(luminaire)

        if photometric_properties.luminous_flux.value:
            self.property_list.add(
                _("Luminous flux"),
                f"{photometric_properties.luminous_flux.value:.0f}lm",
                is_calculated=photometric_properties.luminous_flux.is_calculated,
                hint=_("Total amount of light emitted by the luminaire.")
            )

        if photometric_properties.lor.value:
            self.property_list.append(
                Gauge(
                    name=_("Light output ratio"),
                    value=photometric_properties.lor.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.lor.value:.2%}",
                    calculated=photometric_properties.lor.is_calculated,
                    hint=_("Ratio of luminous flux emitted by the luminaire to the luminous flux emitted by the lamps.")
                )
            )

        if photometric_properties.efficacy.value:
            self.property_list.append(Gauge(
                name=_("Efficacy"),
                min_value=0, max_value=160,
                value=photometric_properties.efficacy.value,
                display=f"{photometric_properties.efficacy.value:.0f}lm/w",
                calculated=photometric_properties.efficacy.is_calculated,
                hint=_("Ratio of luminous flux emitted by the luminaire to the power consumed by the luminaire.")
            ))

        if photometric_properties.dff.value:
            self.property_list.append(
                Gauge(
                    name=_("Downward flux fraction (DFF)"),
                    value=photometric_properties.dff.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.dff.value:.0%}",
                    calculated=photometric_properties.dff.is_calculated,
                    hint=_("Ratio of luminous flux emitted by the luminaire in the downward hemisphere to the luminous flux emitted by the luminaire in all directions.")
                )
            )

        if luminaire.metadata.direct_ratios_for_room_indices:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Direct ratios for room indices"),
                action_name="app.show_direct_ratios",
                activatable_widget=icon,

            )
            row.add_suffix(icon)
            self.property_list.append(row)

        if luminaire.intensity_values:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Intensity values"),
                action_name="app.show_intensity_values",
                activatable_widget=icon,

            )
            row.add_suffix(icon)
            self.property_list.append(row)