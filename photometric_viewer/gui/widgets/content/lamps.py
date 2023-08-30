import re
from typing import List

from gi.repository import Adw
from gi.repository.Gtk import Box, Orientation

from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.gui.widgets.content.temperature import ColorTemperatureGauge
from photometric_viewer.gui.widgets.content.wattage import WattageBox
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.model.settings import Settings


class LampAndBallast(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.view_stack = Adw.ViewStack()

        switcher_bar = Adw.ViewSwitcherBar(
            stack=self.view_stack,
            reveal=True,
            name="lamp-switcher-bar"
        )

        box = Box(
            orientation=Orientation.VERTICAL,
            spacing=8
        )
        box.append(self.view_stack)
        box.append(switcher_bar)

        self.wattage_boxes: List[WattageBox] = []
        self.set_child(box)

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self.view_stack]

        self.wattage_boxes = []
        for child in items:
            self.view_stack.remove(child)

        for n, lamp in enumerate(photometry.lamps):
            property_list = PropertyList()
            property_list.add(_("Number of lamps"), str(lamp.number_of_lamps))
            property_list.add_if_non_empty(_("Lamp"), lamp.description)
            property_list.add_if_non_empty(_("Lamp catalog no."), lamp.catalog_number)

            self._add_color_widget(property_list, lamp.color)

            if lamp.cri and lamp.cri.isnumeric():
                property_list.append(Gauge(
                    name=_("Color Rendering Index (CRI)"),
                    min_value=0, max_value=100,
                    value=float(lamp.cri),
                    display=lamp.cri
                ))
            else:
                property_list.add_if_non_empty(_("Color Rendering Index (CRI)"), lamp.cri)

            if lamp.wattage:
                wattage_box = WattageBox(lamp.wattage)
                property_list.append(wattage_box)
                self.wattage_boxes.append(wattage_box)

            if not photometry.is_absolute:
                property_list.add(_("Initial rating per lamp"), f'{lamp.lumens_per_lamp:.0f}lm')

            property_list.add_if_non_empty(_("Lamp position"), lamp.position)
            property_list.add_if_non_empty(_("Ballast"), lamp.ballast_description)
            property_list.add_if_non_empty(_("Ballast catalog no."), lamp.ballast_catalog_number)

            page_name = lamp.description or _("Lamp {}").format(n)
            page = self.view_stack.add_titled(property_list, "lamp_{n}", page_name)
            page.set_icon_name("io.github.dlippok.photometric-viewer-symbolic")

    def _add_color_widget(self, property_list: PropertyList, color: str | None):
        if not color:
            return

        color_temp_regex = re.compile("^(\\d\\d\\d\\d\\d?)\\s*K?$")
        color_temp_match = color_temp_regex.match(color)

        cri_temp_regex = re.compile("^(\\d)(\\d\\d)$")
        cri_temp_match = cri_temp_regex.match(color)

        if color_temp_match:
            property_list.append(ColorTemperatureGauge(int(color_temp_match.groups()[0])))
        elif cri_temp_match:
            property_list.append(ColorTemperatureGauge(int(cri_temp_match.groups()[1]) * 100))
        else:
            property_list.add(_("Color"), color)

    def update_settings(self, settings: Settings):
        for wattage_box in self.wattage_boxes:
            wattage_box.update_settings(settings)

