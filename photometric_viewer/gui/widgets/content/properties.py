from gi.repository import Gtk
from gi.repository.Gtk import Orientation

from photometric_viewer.gui.widgets.common.header import Header
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire


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
            self.property_list.add(key.title().replace("_", " ").strip(), value)
            children += 1

        self.set_visible(children > 0)
