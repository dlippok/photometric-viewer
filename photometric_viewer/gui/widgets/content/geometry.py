from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry, Shape, LuminousOpeningGeometry, LuminaireGeometry
from photometric_viewer.model.settings import Settings
from photometric_viewer.model.units import LengthUnits, length_factor


class LuminaireGeometryProperties(PropertyList):
    def __init__(self):
        super().__init__()
        self.photometry: Photometry | None = None
        self.settings: Settings | None = None

    def set_photometry(self, photometry: Photometry):
        self.photometry = photometry
        self._refresh_widgets()

    def update_settings(self, settings: Settings):
        self.settings = settings
        self._refresh_widgets()

    def _convert(self, value):
        if not self.settings:
            return f"{value}m"

        if self.settings.length_units_from_file:
            converted_value = value * length_factor(self.photometry.metadata.file_units)
            match self.photometry.metadata.file_units:
                case LengthUnits.METERS:
                    return f"{converted_value:.2f}m"
                case LengthUnits.MILLIMETERS:
                    return f"{converted_value:.0f}mm"
                case LengthUnits.FEET:
                    return f"{converted_value:.2f}ft"
        else:
            converted_value = value * length_factor(self.settings.length_units)
            match self.settings.length_units:
                case LengthUnits.METERS:
                    return f"{converted_value:.2f}m"
                case LengthUnits.CENTIMETERS:
                    return f"{converted_value:.1f}cm"
                case LengthUnits.MILLIMETERS:
                    return f"{converted_value:.0f}mm"
                case LengthUnits.FEET:
                    return f"{converted_value:.2f}ft"
                case LengthUnits.INCHES:
                    return f"{converted_value:.2f}in"

    def _refresh_widgets(self):
        if not self.photometry:
            return

        items = [i for i in self]

        for child in items:
            self.remove(child)

        match self.photometry.luminaire_geometry:
            case LuminaireGeometry(w, l, h, Shape.RECTANGULAR):
                self.add("Luminaire shape", "Rectangular")
                self.add("Luminaire dimensions", f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")
            case LuminaireGeometry(w, l, h, Shape.ROUND):
                self.add("Luminaire shape", "Round")
                self.add("Luminaire dimensions", f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")

        match self.photometry.luminous_opening_geometry:
            case LuminousOpeningGeometry(w, l, Shape.RECTANGULAR):
                self.add("Luminous opening shape", "Rectangular")
                self.add("Luminous opening dimensions", f"{self._convert(w)} x {self._convert(l)}")
            case LuminousOpeningGeometry(w, l, Shape.ROUND):
                self.add("Luminous opening shape", "Round")
                self.add("Luminous opening dimensions", f"{self._convert(w)} x {self._convert(l)}")
