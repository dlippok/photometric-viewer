from gi.repository import Adw, Gtk
from gi.repository.Gtk import Box, Orientation, Label, SelectionMode, Image
from gi.repository.Pango import WrapMode

from photometric_viewer.gui.widgets.common import badges


class PropertyList(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.set_css_classes(["boxed-list"])
        self.set_selection_mode(SelectionMode.NONE)

    @staticmethod
    def _create_item(name, value: str, is_calculated: bool = False, hint: str | None = None):
        row = Adw.ActionRow(
            title=name,
            subtitle=value if (value is not None and value != "") else _("Unknown"),
            css_classes=["property"],
            subtitle_selectable=True
        )

        if is_calculated:
            row.add_suffix(badges.calculated())

        if hint:
            row.add_suffix(badges.info(hint))

        return row

    def add(self, name: str, value: str, is_calculated: bool = False, hint: str | None = None):
        self.append(self._create_item(name=name, value=value, is_calculated=is_calculated, hint=hint))

    def add_expander(self, name: str, value: str, child):
        row = Adw.ExpanderRow(
            title=name,
            subtitle=value if (value is not None and value != "") else _("Unknown"),
            expanded=True,
        )
        row.add_row(child)
        self.append(row)


    def add_if_non_empty(self, name: str, value, hint: str | None = None):
        if value:
            self.append(self._create_item(name=name, value=str(value), hint=hint))

    def clear(self):
        items = [i for i in self]

        for child in items:
            self.remove(child)
