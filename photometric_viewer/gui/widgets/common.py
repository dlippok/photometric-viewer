from gi.repository import Gtk
from gi.repository.Gdk import Clipboard, ContentProvider
from gi.repository.Gtk import Box, Orientation, Label, SelectionMode
from gi.repository.Pango import EllipsizeMode, WrapMode


class PropertyList(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.set_css_classes(["boxed-list"])
        self.set_selection_mode(SelectionMode.NONE)

    def _create_item(self, name, value:str, wrap=False):
        box = Box(orientation=Orientation.VERTICAL)
        box.set_homogeneous(False)
        box.set_spacing(4)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)

        name_label = Label(label=name, hexpand=True, xalign=0)
        name_label.set_css_classes(["h1"])

        displayed_value = value.replace("\n", " ") if wrap else value

        value_label = Label(
            label=displayed_value or "Unknown",
            tooltip_text=value,
            hexpand=True,
            xalign=0,
            selectable=True,
            css_classes=[] if value else ["warning"]
        )

        if wrap:
            value_label.set_wrap(True)
            value_label.set_wrap_mode(WrapMode.WORD_CHAR)
        else:
            value_label.set_ellipsize(EllipsizeMode.END)
            value_label.set_width_chars(16)

        box.append(name_label)
        box.append(value_label)

        return box

    def on_copy_clicked(self, a, value):
        clipboard: Clipboard = self.get_clipboard()
        provider = ContentProvider.new_for_value(value)
        clipboard.set_content(provider)
