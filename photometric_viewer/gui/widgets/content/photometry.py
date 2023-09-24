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
        calculated_properties = calc.calculate_photometric_properties(photometry, photometry.lamps[0])

        lorl = photometry.lorl or round(calculated_properties.lor * 100)
        self.property_list.append(
            Gauge(
                name=_("Light output ratio"),
                value=lorl,
                min_value=0,
                max_value=100,
                display=_value_with_unit(lorl, "%"),
                calculated=photometry.lorl is None
            )
        )

        dff = photometry.dff or round(calculated_properties.dff * 100)
        self.property_list.append(
            Gauge(
                name=_("Downward flux fraction (DFF)"),
                value=dff,
                min_value=0,
                max_value=100,
                display=_value_with_unit(dff, "%"),
                calculated=photometry.dff is None
            )
        )

        if photometry.metadata.conversion_factor:
            self.property_list.add(
                _("Conversion factor for luminous intensities"),
                str(photometry.metadata.conversion_factor)
            )


        if photometry.is_absolute:
            lamp = photometry.lamps[0]

            if lamp.lumens_per_lamp is not None:
                flux_luminaire = round(lamp.lumens_per_lamp * lamp.number_of_lamps)
            else:
                flux_luminaire = round(calculated_properties.flux_luminaire)

            self.property_list.add(
                _("Luminous flux of the luminaire"),
                _value_with_unit(flux_luminaire, "lm"),
                is_calculated=lamp.lumens_per_lamp is None
            )
            print("Calculated:", lamp.lumens_per_lamp is None)

