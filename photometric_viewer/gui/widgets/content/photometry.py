from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.Gtk import Box, Orientation, Label

from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils import calc


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

    def set_photometry(self, luminaire: Luminaire):
        self.property_list.clear()
        photometric_properties = calc.calculate_photometry(luminaire)

        if any((
            photometric_properties.luminous_flux,
            photometric_properties.lor,
            photometric_properties.efficacy,
            photometric_properties.dff
        )):
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Photometric properties"),
                action_name="app.show_photometry",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="photometry-symbolic"))

            if photometric_properties.luminous_flux.value:
                row.add_suffix(Label(label=f"{photometric_properties.luminous_flux.value:.0f} lm"))

            row.add_suffix(icon)
            self.property_list.append(row)

        if luminaire.metadata.direct_ratios_for_room_indices:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Direct ratios for room indices"),
                action_name="app.show_direct_ratios",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="direct-ratios-symbolic"))
            row.add_suffix(icon)
            self.property_list.append(row)

        if luminaire.intensity_values:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Intensity values"),
                action_name="app.show_intensity_values",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="intensities-symbolic"))
            row.add_suffix(icon)
            self.property_list.append(row)

        icon = Gtk.Image(icon_name="go-next-symbolic")
        row = ActionRow(
            title=_("Geometry"),
            action_name="app.show_geometry",
            activatable_widget=icon,
        )
        row.add_prefix(Gtk.Image(icon_name="geometry-symbolic"))
        row.add_suffix(icon)
        self.property_list.append(row)