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
        self.set_visible(False)

        photometric_properties = calc.calculate_photometry(luminaire)

        if any((
            photometric_properties.luminous_flux.value,
            photometric_properties.lor.value,
            photometric_properties.efficacy.value,
            photometric_properties.dff.value
        )):
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Photometric properties"),
                action_name="win.show_photometry",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="photometry-symbolic"))

            if photometric_properties.luminous_flux.value:
                row.add_suffix(Label(label=f"{photometric_properties.luminous_flux.value:.0f} lm"))

            row.add_suffix(icon)
            self.property_list.append(row)
            self.set_visible(True)

        if luminaire.metadata.direct_ratios_for_room_indices:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Direct ratios for room indices"),
                action_name="win.show_direct_ratios",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="direct-ratios-symbolic"))
            row.add_suffix(icon)
            self.property_list.append(row)
            self.set_visible(True)

        if luminaire.intensity_values:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Intensity values"),
                action_name="win.show_intensity_values",
                activatable_widget=icon,

            )
            row.add_prefix(Gtk.Image(icon_name="intensities-symbolic"))
            row.add_suffix(icon)
            self.property_list.append(row)
            self.set_visible(True)

        if luminaire.geometry or luminaire.luminous_opening_geometry:
            icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=_("Geometry"),
                action_name="win.show_geometry",
                activatable_widget=icon,
            )
            row.add_prefix(Gtk.Image(icon_name="geometry-symbolic"))
            row.add_suffix(icon)
            self.property_list.append(row)
            self.set_visible(True)