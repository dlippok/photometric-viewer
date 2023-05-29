from gi.repository import Adw
from gi.repository.Gtk import Box, Orientation

from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


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
        self.set_child(box)

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self.view_stack]

        for child in items:
            self.view_stack.remove(child)

        for n, lamp in enumerate(photometry.lamps):
            property_list = PropertyList()
            property_list.add("Number of lamps", str(lamp.number_of_lamps))
            property_list.add_if_non_empty("Lamp", lamp.description)
            property_list.add_if_non_empty("Lamp catalog no.", lamp.catalog_number)
            property_list.add_if_non_empty("Color", lamp.color)
            property_list.add_if_non_empty("Color Rendering Index (CRI)", lamp.cri)
            property_list.add_if_non_empty("Wattage", lamp.wattage)

            if not photometry.is_absolute:
                property_list.add("Initial rating per lamp", f'{lamp.lumens_per_lamp:.0f}lm')

            property_list.add_if_non_empty("Lamp position", lamp.position)
            property_list.add_if_non_empty("Ballast", lamp.ballast_description)
            property_list.add_if_non_empty("Ballast catalog no.", lamp.ballast_catalog_number)

            page_name = lamp.description or f"Lamp {n}"
            page = self.view_stack.add_titled(property_list, f"lamp_{n}", page_name)
            page.set_icon_name("io.github.dlippok.photometrics-viewer-symbolic")
