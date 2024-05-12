from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.GLib import Variant

from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire


class LampAndBallast(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.luminaire: Luminaire | None = None

        self.property_list = PropertyList()
        self.append(Header(label=_("Lamps and ballast"), xalign=0))
        self.append(self.property_list)
        self.set_visible(False)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self._refresh_widgets()

    def _refresh_widgets(self):
        self.set_visible(False)

        self.property_list.clear()
        if not self.luminaire:
            return

        for i, lamp_set in enumerate(self.luminaire.lamps[:30]):
            if all(v is None for k, v in lamp_set.__dict__.items()):
                continue

            action_icon = Gtk.Image(icon_name="go-next-symbolic")
            row = ActionRow(
                title=f"{lamp_set.number_of_lamps or 1} x {lamp_set.description or _('Lamp')}",
                activatable_widget=action_icon,
                action_name="win.show_lamp_set",
                action_target=Variant.new_int32(i)
            )
            row.add_prefix(Gtk.Image(icon_name="lamp-symbolic"))
            row.add_suffix(action_icon)
            self.property_list.append(row)
            self.set_visible(True)

            if lamp_set.ballast_description or lamp_set.ballast_catalog_number:
                action_icon = Gtk.Image(icon_name="go-next-symbolic")
                row = ActionRow(
                    title=lamp_set.ballast_description or _('Ballast'),
                    activatable_widget=action_icon,
                    action_name="win.show_ballast",
                    action_target=Variant.new_int32(i)
                )
                row.add_prefix(Gtk.Image(icon_name="ballast-symbolic"))
                row.add_suffix(action_icon)
                self.property_list.append(row)
                self.set_visible(True)

