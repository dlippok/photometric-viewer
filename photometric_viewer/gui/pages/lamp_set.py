import re

from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.gui.widgets.content.photometry import _value_with_unit
from photometric_viewer.gui.widgets.content.temperature import ColorTemperatureGauge
from photometric_viewer.gui.widgets.content.wattage import WattageBox
from photometric_viewer.model.luminaire import Lamps, Luminaire


class LampSetPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__("", **kwargs)
        self.property_list = PropertyList()
        self.wattage_box = None
        self.append(self.property_list)
    def set_lamp_set(self, luminaire: Luminaire, lamp_set: Lamps):
        self.property_list.clear()
        self.set_title(f"{lamp_set.number_of_lamps or 1} x {lamp_set.description or _('Lamp')}")

        self.property_list.add_if_non_empty(_("Number of lamps"), lamp_set.number_of_lamps)
        self.property_list.add_if_non_empty(_("Lamp"), lamp_set.description)
        self.property_list.add_if_non_empty(_("Lamp catalog no."), lamp_set.catalog_number)

        self._add_color_widget(lamp_set)
        self._add_cri_widget(lamp_set)
        self._add_wattage_widget(lamp_set)

        if not luminaire.photometry.is_absolute and lamp_set.lumens_per_lamp:
            self.property_list.add(
                _("Initial rating per lamp"),
                f'{lamp_set.lumens_per_lamp:.0f}lm',
                hint=_("Luminous flux emitted by the lamp.")
            )

            if lamp_set.wattage:
                efficacy = round(lamp_set.lumens_per_lamp * lamp_set.number_of_lamps / lamp_set.wattage)
                self.property_list.append(Gauge(
                    name=_("Efficacy"),
                    min_value=0, max_value=160,
                    value=efficacy,
                    display=_value_with_unit(efficacy, "lm/W"),
                    calculated=lamp_set.lumens_per_lamp is None,
                    hint=_("Ratio of luminous flux emitted by the lamp to the power consumed by the lamp.")
                ))

        self.property_list.add_if_non_empty(_("Lamp position"), lamp_set.position)

    def _add_color_widget(self, lamp_set: Lamps):
        if not lamp_set.color:
            return

        color_temp_regex = re.compile("^(\\d\\d\\d\\d\\d?)\\s*K?$")
        color_temp_match = color_temp_regex.match(lamp_set.color)

        cri_temp_regex = re.compile("^(\\d)(\\d\\d)$")
        cri_temp_match = cri_temp_regex.match(lamp_set.color)

        if color_temp_match:
            self.property_list.append(ColorTemperatureGauge(int(color_temp_match.groups()[0])))
        elif cri_temp_match:
            self.property_list.append(ColorTemperatureGauge(int(cri_temp_match.groups()[1]) * 100))
        else:
            self.property_list.add(
                _("Color"),
                lamp_set.color,
                hint=_("Light color as specified by the manufacturer.")
            )

    def _add_cri_widget(self, lamp_set: Lamps):
        if lamp_set.cri and lamp_set.cri.isnumeric():
            self.property_list.append(
                Gauge(
                    name=_("Color Rendering Index (CRI)"),
                    min_value=0, max_value=100,
                    value=float(lamp_set.cri),
                    display=lamp_set.cri,
                    hint=_(
                        "Measure of the ability of a light source to reproduce the colors of various objects faithfully in comparison with an ideal or natural light source."
                    )
                )
            )
        else:
            self.property_list.add_if_non_empty(
                _("Color Rendering Index (CRI)"),
                lamp_set.cri,
                hint=_(
                    "Measure of the ability of a light source to reproduce the colors of various objects faithfully in comparison with an ideal or natural light source."
                )
            )

    def _add_wattage_widget(self, lamp_set: Lamps):
        self.wattage_box = None
        if lamp_set.wattage:
            self.wattage_box = WattageBox(lamp_set.wattage)
            self.property_list.append(self.wattage_box)

