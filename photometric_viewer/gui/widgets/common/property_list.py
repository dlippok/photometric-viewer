from gi.repository import Gtk
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
        box = Box(orientation=Orientation.VERTICAL)
        box.set_homogeneous(False)
        box.set_spacing(4)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)

        name_box = Box(orientation=Orientation.HORIZONTAL)
        name_label = Label(label=name, hexpand=True, xalign=0, wrap=True, wrap_mode=WrapMode.WORD_CHAR)
        name_label.set_css_classes(["h1"])
        name_box.append(name_label)

        if is_calculated:
            name_box.append(badges.calculated())

        box.append(name_box)

        if hint:
            hint_label = Label(
                label=hint,
                hexpand=True,
                xalign=0,
                wrap=True,
                wrap_mode=WrapMode.WORD_CHAR,
                selectable=True,
                css_classes=["dim-label"],
            )
            box.append(hint_label)

        value_label = Label(
            label=value if (value is not None and value != "") else _("Unknown"),
            margin_top=8,
            tooltip_text=value,
            hexpand=True,
            xalign=0,
            selectable=True,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            css_classes=[] if (value is not None and value != "") else ["warning"],
        )

        box.append(value_label)

        return box

    def add(self, name: str, value: str, is_calculated: bool = False, hint: str | None = None):
        self.append(self._create_item(name=name, value=value, is_calculated=is_calculated, hint=hint))

    def add_if_non_empty(self, name: str, value, hint: str | None = None):
        if value:
            self.append(self._create_item(name=name, value=value, hint=hint))

    def clear(self):
        items = [i for i in self]

        for child in items:
            self.remove(child)
