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

        self.append(self._create_item(name="Number of lamps", value=str(photometry.lamps.number_of_lamps)))
        self._create_if_exists("Lamp", photometry.lamps.description)
        self._create_if_exists("Lamp catalog no.", photometry.lamps.catalog_number)

        if not photometry.lamps.is_absolute:
            self.append(self._create_item(name="Initial rating per lamp", value=f'{photometry.lamps.lumens_per_lamp:.0f}lm'))

        self._create_if_exists("Lamp position", photometry.lamps.position)

        self._create_if_exists("Ballast", photometry.ballast.description)
        self._create_if_exists("Ballast catalog no.", photometry.ballast.catalog_number)

