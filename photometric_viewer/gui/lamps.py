from photometric_viewer.gui.widgets.common import PropertyList
from photometric_viewer.model.photometry import Photometry


class LampAndBallast(PropertyList):
    def _create_if_exists(self, key, value):
        if value:
            self.append(self._create_item(name=key, value=value))

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        for lamp in photometry.lamps:
            self.append(self._create_item(name="Number of lamps", value=str(lamp.number_of_lamps)))
            self._create_if_exists("Lamp", lamp.description)
            self._create_if_exists("Lamp catalog no.", lamp.catalog_number)
            self._create_if_exists("Color", lamp.color)
            self._create_if_exists("Color Rendering Index (CRI)", lamp.cri)
            self._create_if_exists("Wattage", lamp.wattage)

            if not photometry.is_absolute:
                self.append(self._create_item(name="Initial rating per lamp", value=f'{lamp.lumens_per_lamp:.0f}lm'))

            self._create_if_exists("Lamp position", lamp.position)
            self._create_if_exists("Ballast", lamp.ballast_description)
            self._create_if_exists("Ballast catalog no.", lamp.ballast_catalog_number)

