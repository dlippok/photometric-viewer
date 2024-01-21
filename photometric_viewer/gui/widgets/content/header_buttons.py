from gi.overrides.Gtk import Builder
from gi.repository import Gio, Gtk
from gi.repository.GLib import Variant
from gi.repository.Gtk import Box, Orientation, MenuButton

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.urls import is_url

MENU_MODELS = """
<?xml version="1.0"?>
<interface>
    <menu id='header-menu-export'>
        <section>
            <item>
                <attribute name='label' translatable='yes'>As EULUMDAT</attribute>
                <attribute name='action'>app.export_as_ldt</attribute>
            </item>
            <item>
                <attribute name='label' translatable='yes'>As IESNA</attribute>
                <attribute name='action'>app.export_as_ies</attribute>
            </item>
            <item>
                <attribute name='label' translatable='yes'>Light distribution curve</attribute>
                <attribute name='action'>app.export_ldc_as_image</attribute>
            </item>
            <item>
                <attribute name='label' translatable='yes'>Intensity values</attribute>
                <attribute name='action'>app.export_intensities_as_csv</attribute>
            </item>
            <item>
                <attribute name='label' translatable='yes'>Luminaire data</attribute>
                <attribute name='action'>app.export_luminaire_as_json</attribute>
            </item>
        </section>
    </menu>
    <menu id='header-menu-other'>
        <section>
            <item>
                <attribute name='label' translatable='yes'>Intensity Values</attribute>
                <attribute name='action'>app.show_intensity_values</attribute>
            </item>
            <item>
                <attribute name='label' translatable='yes'>Show source</attribute>
                <attribute name='action'>app.show_source</attribute>
            </item>
        </section>
    </menu>
    
</interface>
"""



class HeaderButtons(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.HORIZONTAL,
            spacing=8,
        )

        builder: Builder = Builder()
        builder.set_translation_domain("io.github.dlippok.photometric-viewer")
        builder.add_from_string(MENU_MODELS)

        export_button = MenuButton(
            icon_name="document-save-as-symbolic",
            menu_model=builder.get_object("header-menu-export"),
            css_classes=["circular"],
            tooltip_text=_("Export")
        )

        self.url_button = MenuButton(
            icon_name = "web-browser-symbolic",
            css_classes=["circular"],
            tooltip_text=_("Open in browser"),
            visible=False
        )

        other_menu_button = MenuButton(
            icon_name="open-menu",
            menu_model=builder.get_object("header-menu-other"),
            css_classes=["circular"],
            tooltip_text=_("Menu")
        )

        self.append(export_button)
        self.append(self.url_button)
        self.append(other_menu_button)

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
            item.set_action_and_target_value('app.open_url', Variant.new_string(url))
            menu.append_item(item)

        self.url_button.set_menu_model(menu)
        self.url_button.set_visible(bool(urls))


