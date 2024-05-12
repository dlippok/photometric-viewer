from gi.repository import Gio
from gi.repository.Adw import ButtonContent
from gi.repository.GLib import Variant
from gi.repository.Gtk import Box, Orientation, MenuButton, Button

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.urls import is_url


class HeaderButtons(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.HORIZONTAL,
            spacing=8,
        )

        self.url_button = MenuButton(
            icon_name = "web-browser-symbolic",
            css_classes=["circular"],
            tooltip_text=_("Open in browser"),
            visible=False
        )

        edit_source_button = Button(
            css_classes=["pill"],
            tooltip_text=_("Menu"),
            action_name="win.show_source"

        )
        edit_source_button.set_child(
            ButtonContent(
                icon_name="document-edit-symbolic",
                label=_("Edit source"),
            )
        )

        self.append(self.url_button)
        self.append(edit_source_button)

    def set_photometry(self, luminaire: Luminaire):
        urls = {
            key: value
            for key, value
            in luminaire.metadata.additional_properties.items()
            if is_url(value)
        }

        menu = Gio.Menu()

        for label, url in urls.items():
            display_label = label.title().replace("_", " ").strip()
            item = Gio.MenuItem()
            item.set_label(display_label)
            item.set_action_and_target_value('win.open_url', Variant.new_string(url))
            menu.append_item(item)

        self.url_button.set_menu_model(menu)
        self.url_button.set_visible(bool(urls))


