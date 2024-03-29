from gi.repository import Gtk
from gi.repository.Adw import ActionRow
from gi.repository.Gtk import Orientation

from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.urls import is_url


class LuminaireProperties(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.VERTICAL,
            spacing=16
        )
        self.property_list = PropertyList()
        self.append(Header(label=_("Additional properties"), xalign=0))
        self.append(self.property_list)

    def set_photometry(self, luminaire: Luminaire):
        self.property_list.clear()
        children = 0
        for key, value in luminaire.metadata.additional_properties.items():
            if is_url(value):
                continue

            row = ActionRow(
                title=key.title().replace("_", " ").strip(),
                subtitle=value,
                title_selectable=True,
                subtitle_selectable=True,
                css_classes=["property"] if value else []

            )

            self.property_list.append(row)
            children += 1

        self.set_visible(children > 0)

