from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.GLib import Variant
from gi.repository.Gtk import Orientation

from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.urls import is_url
from photometric_viewer.profiling.decorators import profiled


class LuminaireProperties(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.VERTICAL,
            spacing=16
        )

        self.luminaire: Luminaire = None

        self.property_list = PropertyList()
        self.append(Header(label=_("Additional properties"), xalign=0))
        self.append(self.property_list)

    @profiled()
    def set_photometry(self, luminaire: Luminaire):
        self.property_list.remove_all()

        for key, value in luminaire.metadata.additional_properties.items():
                row = ActionRow(
                    title=key.title().replace("_", " ").strip(),
                    subtitle=value,
                    title_selectable=True,
                    subtitle_selectable=True,
                    css_classes=["property"] if value else []

                )

                if is_url(value):
                    url_icon = Gtk.Image(icon_name='web-browser-symbolic')
                    row.add_suffix(url_icon)
                    row.set_activatable(True)
                    row.set_action_name('win.open_url')
                    row.set_action_target_value(Variant.new_string(value))
                else:
                    row.set_activatable(False)

                self.property_list.append(row)


        self.set_visible(len(luminaire.metadata.additional_properties) > 0)
