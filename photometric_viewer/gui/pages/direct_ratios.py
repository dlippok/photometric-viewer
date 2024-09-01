from gi.repository.Adw import ActionRow

from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire


class DirectRatiosPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__(_("Direct ratios for room indices"), **kwargs)
        self.luminaire = None
        self.property_list = PropertyList()
        self.append(self.property_list)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.property_list.clear()

        for room_index, ratio in luminaire.metadata.direct_ratios_for_room_indices.items():
            row = ActionRow(
                title=_("Room index: {:.2f}").format(room_index),
                subtitle=f"{ratio:.3f}",
                css_classes=["property"],
                subtitle_selectable=True

            )
            self.property_list.append(row)
