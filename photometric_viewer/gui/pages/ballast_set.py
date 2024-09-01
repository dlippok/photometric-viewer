from photometric_viewer.gui.pages.base import SidebarPage
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Lamps


class BallastPage(SidebarPage):
    def __init__(self, **kwargs):
        super().__init__(_("Ballast"), **kwargs)
        self.property_list = PropertyList()
        self.append(self.property_list)

    def set_lamp_set(self, lamp_set: Lamps):
        self.property_list.clear()
        self.set_title(lamp_set.ballast_description or _('Ballast'))

        self.property_list.add_if_non_empty(_("Ballast"), lamp_set.ballast_description)
        self.property_list.add_if_non_empty(_("Ballast catalog no."), lamp_set.ballast_catalog_number)
