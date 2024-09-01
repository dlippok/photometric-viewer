from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import (Luminaire, LuminousOpeningShape, LuminousOpeningGeometry,
                                                LuminaireType, LuminaireGeometry, Shape)
from photometric_viewer.model.units import LengthUnits, length_factor
from photometric_viewer.utils.gi.GSettings import SettingsManager


class GeometryPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__(_("Geometry"), **kwargs)
        self.luminaire: Luminaire | None = None
        self.property_list = PropertyList()
        self.append(self.property_list)

        self.settings_manager = SettingsManager()
        self.settings_manager.register_on_update(lambda *args: self._refresh_widgets())

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self._refresh_widgets()

    def _convert(self, value):
        if not self.settings_manager.settings:
            return f"{value}m"

        if self.settings_manager.settings.length_units_from_file:
            converted_value = value * length_factor(self.luminaire.metadata.file_units)
            match self.luminaire.metadata.file_units:
                case LengthUnits.METERS:
                    return f"{converted_value:.2f}m"
                case LengthUnits.MILLIMETERS:
                    return f"{converted_value:.0f}mm"
                case LengthUnits.FEET:
                    return f"{converted_value:.2f}ft"
        else:
            converted_value = value * length_factor(self.settings_manager.settings.length_units)
            match self.settings_manager.settings.length_units:
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
        if not self.luminaire:
            return

        self.property_list.clear()

        match self.luminaire.geometry:
            case LuminaireGeometry(w, l, h, Shape.RECTANGULAR):
                self.property_list.add(_("Luminaire shape"), _("Rectangular"))
                self.property_list.add(_("Luminaire dimensions"), f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")
            case LuminaireGeometry(w, l, h, Shape.ROUND):
                self.property_list.add(_("Luminaire shape"), _("Round"))
                self.property_list.add(_("Luminaire dimensions"), f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")

        if self.luminaire.luminous_opening_geometry is not None:
            match self.luminaire.luminous_opening_geometry.shape:
                case LuminousOpeningShape.RECTANGULAR:
                    self.property_list.add(_("Luminous opening shape"), _("Rectangular"))
                case LuminousOpeningShape.ROUND:
                    self.property_list.add(_("Luminous opening shape"), _("Round"))
                case LuminousOpeningShape.SPHERE:
                    self.property_list.add(_("Luminous opening shape"), _("Sphere"))
                case LuminousOpeningShape.POINT:
                    self.property_list.add(_("Luminous opening shape"), _("Point"))
                case LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_WIDTH:
                    self.property_list.add(_("Luminous opening shape"), _("Horizontal cylinder oriented along luminaire width"))
                case LuminousOpeningShape.HORIZONTAL_CYLINDER_ALONG_LENGTH:
                    self.property_list.add(_("Luminous opening shape"), _("Horizontal cylinder oriented along luminaire length"))
                case LuminousOpeningShape.ELLIPSE_ALONG_WIDTH:
                    self.property_list.add(_("Luminous opening shape"), _("Ellipse oriented along luminaire width"))
                case LuminousOpeningShape.ELLIPSE_ALONG_LENGTH:
                    self.property_list.add(_("Luminous opening shape"), _("Ellipse oriented along luminaire length"))
                case LuminousOpeningShape.ELLIPSOID_ALONG_WIDTH:
                    self.property_list.add(_("Luminous opening shape"), _("Ellipsoid oriented along luminaire width"))
                case LuminousOpeningShape.ELLIPSOID_ALONG_LENGTH:
                    self.property_list.add(_("Luminous opening shape"), _("Ellipsoid oriented along luminaire length"))

            match self.luminaire.luminous_opening_geometry:
                case LuminousOpeningGeometry(width=0, length=0, height=0, shape=LuminousOpeningShape.POINT):
                    pass
                case LuminousOpeningGeometry(width=w, length=l, height=0, shape=_):
                    self.property_list.add(_("Luminous opening dimensions"), f"{self._convert(w)} x {self._convert(l)}")
                case LuminousOpeningGeometry(width=w, length=l, height=h, height_c90=None, shape=_):
                    self.property_list.add(_("Luminous opening dimensions"),
                             f"{self._convert(w)} x {self._convert(l)} x {self._convert(h)}")
                case LuminousOpeningGeometry(width=w, length=l, height=h0, height_c90=h90, height_c180=h180,
                                             height_c270=h270, shape=_):
                    self.property_list.add(_("Luminous opening dimensions"), f"{self._convert(w)} x {self._convert(l)}")
                    self.property_list.add(
                        _("Luminous opening height"),
                        f"C0:\t\t{self._convert(h0)}\nC90:\t{self._convert(h90)}\nC180:\t{self._convert(h180)}\nC270:\t{self._convert(h270)}"
                    )

        self.property_list.add_if_non_empty(_("Luminaire type"), self._display_luminaire_type(self.luminaire.metadata.luminaire_type))

    @staticmethod
    def _display_luminaire_type(luminaire_type: LuminaireType | None):
        match luminaire_type:
            case LuminaireType.POINT_SOURCE_WITH_VERTICAL_SYMMETRY:
                return _("Point source with symmetry about the vertical axis")
            case LuminaireType.LINEAR:
                return _("Linear luminaire")
            case LuminaireType.POINT_SOURCE_WITH_OTHER_SYMMETRY:
                return _("Point source with any other symmetry")
            case None:
                return None
