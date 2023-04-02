from gi.repository import Gtk
from gi.repository.Gdk import Clipboard, ContentProvider
from gi.repository.Gtk import Box, Orientation, Label, SelectionMode, Button
from gi.repository.Pango import EllipsizeMode

from photometric_viewer.model.photometry import Photometry


class LuminaireProperties(Gtk.ListBox):
    def __init__(self):
        super().__init__()
        self.set_css_classes(["boxed-list"])
        self.set_selection_mode(SelectionMode.NONE)

    def _create_item(self, name, value):
        box = Box(orientation=Orientation.HORIZONTAL)
        box.set_spacing(128)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)

        name_label = Label(label=name, hexpand=True, xalign=0)

        value_label = Label(
            label=value or "Unknown",
            hexpand=True,
            xalign=1,
            css_classes=[] if value else ["warning"]
        )
        value_label.set_ellipsize(EllipsizeMode.END)
        value_label.set_tooltip_text(value)
        value_label.set_width_chars(8)

        copy_button: Button = Button.new_from_icon_name("edit-copy")
        copy_button.connect("clicked", self.on_copy_clicked, value)

        value_box = Box(orientation=Orientation.HORIZONTAL, spacing=16)
        value_box.append(value_label)
        value_box.append(copy_button)

        box.append(name_label)
        box.append(value_box)

        return box

    def on_copy_clicked(self, a, value):
        clipboard: Clipboard = self.get_clipboard()
        provider = ContentProvider.new_for_value(value)
        clipboard.set_content(provider)

    def set_photometry(self, photometry: Photometry):
        items = [i for i in self]

        for child in items:
            self.remove(child)

        self.append(self._create_item(name="Name", value=photometry.metadata.luminaire))
        self.append(self._create_item(name="Manufacturer", value=photometry.metadata.manufacturer))

        for key, value in photometry.metadata.additional_properties.items():
            self.append(self._create_item(name=key, value=value))
