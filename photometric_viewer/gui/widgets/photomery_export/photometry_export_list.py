import dataclasses

from gi.repository import Adw, Gtk
from gi.repository.Gtk import SelectionMode


@dataclasses.dataclass
class LdtExportProperties:
    pass

@dataclasses.dataclass
class IesExportProperties:
    pass

class PhotometryExportList(Gtk.ListBox):
    def __init__(self):
        super().__init__(
            css_classes=["boxed-list"],
            selection_mode=SelectionMode.NONE
        )

        self.format_selection_row = Adw.ComboRow(
            title=_("Format"),
            model = Gtk.StringList.new(
                [
                    _("EULUMDAT"),
                    _("IES")
                ]
            )
        )
        self.append(self.format_selection_row)

    def get_current_properties(self):
        if self.format_selection_row.get_selected() == 0:
            return LdtExportProperties()
        else:
            return IesExportProperties()