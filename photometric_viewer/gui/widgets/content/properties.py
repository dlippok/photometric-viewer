from gi.repository import Gtk
from gi.repository.Adw import ActionRow
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
        properties = [(k, v) for k, v in luminaire.metadata.additional_properties.items()]

        list_item_len = len(list(self.property_list))
        additional_properties_len = len(properties)

        to_remove = []

        for i in range(max(list_item_len, additional_properties_len)):
            if i >= list_item_len:
                key, value = properties[i]

                row = ActionRow(
                    title=key.title().replace("_", " ").strip(),
                    subtitle=value,
                    title_selectable=True,
                    subtitle_selectable=True,
                    css_classes=["property"] if value else []

                )
                self.property_list.append(row)

            elif i >= additional_properties_len:
                row = list(self.property_list)[i]
                to_remove.append(row)

            else:
                key, value = properties[i]
                row: ActionRow = list(self.property_list)[i]
                row.set_title(key.title().replace("_", " ").strip())
                row.set_subtitle(value)

        for row in to_remove:
            self.property_list.remove(row)

        self.set_visible(additional_properties_len > 0)

    def _needs_update(self, luminaire: Luminaire):
        return True
