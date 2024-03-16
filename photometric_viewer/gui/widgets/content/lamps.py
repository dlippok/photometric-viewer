from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.GLib import Variant

from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire


class LampAndBallast(PropertyList):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.luminaire: Luminaire | None = None

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self._refresh_widgets()

    def _refresh_widgets(self):
        self.clear()
        if not self.luminaire:
            return

        for i, lamp_set in enumerate(self.luminaire.lamps[:30]):
            action_icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=f"{lamp_set.number_of_lamps or 1} x {lamp_set.description or _('Lamp')}",
                activatable_widget=action_icon,
                action_name="app.show_lamp_set",
                action_target=Variant.new_int32(i)
            )
            row.add_prefix(Gtk.Image(icon_name="lamp-symbolic"))
            row.add_suffix(action_icon)
            self.append(row)

            if lamp_set.ballast_description or lamp_set.ballast_catalog_number:
                action_icon = Gtk.Image(icon_name="go-next-symbolic")
                row = ActionRow(
                    title=lamp_set.ballast_description or _('Ballast'),
                    activatable_widget=action_icon,
                    action_name="app.show_ballast",
                    action_target=Variant.new_int32(i)
                )
                row.add_prefix(Gtk.Image(icon_name="ballast-symbolic"))
                row.add_suffix(action_icon)
                self.append(row)

