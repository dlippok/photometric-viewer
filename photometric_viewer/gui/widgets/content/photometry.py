from gi.repository.Gtk import Box, Orientation

from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry


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

        visible = False
        if photometry.lorl:
            visible = True
            self.property_list.append(
                Gauge(
                    name=_("Light output ratio"),
                    value=photometry.lorl,
                    min_value=0,
                    max_value=100,
                    display=_value_with_unit(photometry.lorl, "%")
                )
            )

        if photometry.dff:
            visible = True
            self.property_list.append(
                Gauge(
                    name=_("Downward flux fraction (DFF)"),
                    value=photometry.dff,
                    min_value=0,
                    max_value=100,
                    display=_value_with_unit(photometry.dff, "%")
                )
            )

        if photometry.metadata.conversion_factor:
            visible = True
            self.property_list.add(
                _("Conversion factor for luminous intensities"),
                str(photometry.metadata.conversion_factor)
            )

        self.set_visible(visible)
