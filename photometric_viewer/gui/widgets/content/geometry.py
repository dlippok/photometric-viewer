from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry, Shape, LuminousOpeningGeometry, LuminaireGeometry, \
    LuminousOpeningShape
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
                self.add(_("Luminaire shape"), _("Rectangular"))
                self.add(_("Luminaire dimensions"), f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")
            case LuminaireGeometry(w, l, h, Shape.ROUND):
                self.add(_("Luminaire shape"), _("Round"))
                self.add(_("Luminaire dimensions"), f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")

        match self.photometry.luminous_opening_geometry.shape:
            case LuminousOpeningShape.RECTANGULAR:
                self.add(_("Luminous opening shape"), _("Rectangular"))
            case LuminousOpeningShape.ROUND:
                self.add(_("Luminous opening shape"), _("Round"))
            case LuminousOpeningShape.SPHERE:
                self.add(_("Luminous opening shape"), _("Sphere"))
            case LuminousOpeningShape.POINT:
                self.add(_("Luminous opening shape"), _("Point"))
            case LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH:
                self.add(_("Luminous opening shape"), _("Horizontal cylinder oriented along luminaire width"))
            case LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH:
                self.add(_("Luminous opening shape"), _("Horizontal cylinder oriented along luminaire length"))
            case LuminousOpeningShape.ELLIPSE_ALONG_WIDTH:
                self.add(_("Luminous opening shape"), _("Ellipse oriented along luminaire width"))
            case LuminousOpeningShape.ELLIPSE_ALONG_LENGTH:
                self.add(_("Luminous opening shape"), _("Ellipse oriented along luminaire length"))
            case LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH:
                self.add(_("Luminous opening shape"), _("Ellipsoid oriented along luminaire width"))
            case LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH:
                self.add(_("Luminous opening shape"), _("Ellipsoid oriented along luminaire length"))

        match self.photometry.luminous_opening_geometry:
            case LuminousOpeningGeometry(width=0, length=0, height=0, shape=LuminousOpeningShape.POINT):
                pass
            case LuminousOpeningGeometry(width=w, length=l, height=0, shape=_):
                self.add(_("Luminous opening dimensions"), f"{self._convert(w)} x {self._convert(l)}")
            case LuminousOpeningGeometry(width=w, length=l, height=h, height_c90=None, shape=_):
                self.add(_("Luminous opening dimensions"), f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")
            case LuminousOpeningGeometry(width=w, length=l, height=h0, height_c90=h90, height_c180=h180, height_c270=h270, shape=_):
                self.add(_("Luminous opening dimensions"), f"{self._convert(w)} x {self._convert(l)}")
                self.add(
                    _("Luminous opening height"),
                    f"C0:\t\t{self._convert(h0)}\nC90:\t{self._convert(h90)}\nC180:\t{self._convert(h180)}\nC270:\t{self._convert(h270)}"
                )
