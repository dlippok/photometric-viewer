from gi.repository.Gtk import Box, Orientation

from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry
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

    def set_photometry(self, photometry: Photometry):
        self.property_list.clear()
        photometric_properties = calc.calculate_luminaire_photometric_properties(photometry)

        if photometric_properties.lor.value:
            self.property_list.append(
                Gauge(
                    name=_("Light output ratio"),
                    value=photometric_properties.lor.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.lor.value:.2%}",
                    calculated=photometric_properties.lor.is_calculated
                )
            )

        if photometric_properties.dff.value:
            self.property_list.append(
                Gauge(
                    name=_("Downward flux fraction (DFF)"),
                    value=photometric_properties.dff.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.lor.value:.0%}",
                    calculated=photometric_properties.dff.is_calculated
                )
            )

        if photometry.metadata.conversion_factor:
            self.property_list.add(
                _("Conversion factor for luminous intensities"),
                str(photometry.metadata.conversion_factor)
            )

        if photometric_properties.luminous_flux.value:
            self.property_list.add(
                _("Luminous flux of the luminaire"),
                f"{photometric_properties.luminous_flux.value:.0f}lm",
                is_calculated=photometric_properties.luminous_flux.is_calculated
            )

        if photometric_properties.efficacy.value:
            self.property_list.append(Gauge(
                name=_("Efficacy"),
                min_value=0, max_value=160,
                value=photometric_properties.efficacy.value,
                display=f"{photometric_properties.efficacy.value:.0f}lm/w",
                calculated=photometric_properties.efficacy.is_calculated
            ))
