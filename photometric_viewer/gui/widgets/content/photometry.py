from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.Gtk import Box, Orientation, Label

from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils import calc
from photometric_viewer.profiling.decorators import profiled


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
        self.append(self.property_list)

        photometric_properites_icon = Gtk.Image(icon_name="go-next-symbolic")
        self.photometric_properites_row = ActionRow(
            title=_("Photometric properties"),
            action_name="win.show_photometry",
            activatable_widget=photometric_properites_icon,
        )
        self.photometric_properites_flux_label = Label()
        self.photometric_properites_row.add_suffix(self.photometric_properites_flux_label)
        self.photometric_properites_row.add_suffix(photometric_properites_icon)
        self.property_list.append(self.photometric_properites_row)

        icon = Gtk.Image(icon_name="go-next-symbolic")
        self.direct_ratios_row = ActionRow(
                title=_("Direct ratios for room indices"),
                action_name="win.show_direct_ratios",
                activatable_widget=icon,

            )
        self.direct_ratios_row.add_prefix(Gtk.Image(icon_name="direct-ratios-symbolic"))
        self.direct_ratios_row.add_suffix(icon)
        self.property_list.append(self.direct_ratios_row)

        icon = Gtk.Image(icon_name="go-next-symbolic")
        self.intensity_values_row = ActionRow(
            title=_("Intensity values"),
            action_name="win.show_intensity_values",
            activatable_widget=icon,

        )
        self.intensity_values_row.add_prefix(Gtk.Image(icon_name="intensities-symbolic"))
        self.intensity_values_row.add_suffix(icon)
        self.property_list.append(self.intensity_values_row)

        icon = Gtk.Image(icon_name="go-next-symbolic")
        self.geometry_row = ActionRow(
            title=_("Geometry"),
            action_name="win.show_geometry",
            activatable_widget=icon,
        )
        self.geometry_row.add_prefix(Gtk.Image(icon_name="geometry-symbolic"))
        self.geometry_row.add_suffix(icon)
        self.property_list.append(self.geometry_row)

    @profiled()
    def set_photometry(self, luminaire: Luminaire):
        photometric_properties = calc.PHOTOMETRIC_PROPERTY_CALCULATOR.calculate(luminaire)

        photometric_properties_visible = any((
                photometric_properties.luminous_flux.value,
                photometric_properties.lor.value,
                photometric_properties.efficacy.value,
                photometric_properties.dff.value
        ))

        self.photometric_properites_row.set_visible(photometric_properties_visible)

        if photometric_properties.luminous_flux.value:
                self.photometric_properites_flux_label.set_label(f"{photometric_properties.luminous_flux.value:.0f} lm")
                self.photometric_properites_flux_label.set_visible(True)
        else:
                self.photometric_properites_flux_label.set_visible(False)

        if luminaire.metadata.direct_ratios_for_room_indices:
            self.direct_ratios_row.set_visible(True)
        else:
            self.direct_ratios_row.set_visible(False)

        if luminaire.intensity_values:
            self.intensity_values_row.set_visible(True)
        else:
            self.intensity_values_row.set_visible(False)

        if luminaire.geometry or luminaire.luminous_opening_geometry:
            self.geometry_row.set_visible(True)
        else:
            self.geometry_row.set_visible(False)

        self.set_visible(
            any((
                self.photometric_properites_row.get_visible(),
                self.direct_ratios_row.get_visible(),
                self.intensity_values_row.get_visible(),
                self.geometry_row.get_visible(),
            ))
        )

