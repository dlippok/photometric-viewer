import datetime

from gi.repository import Gtk


class ApplicationMenuButton(Gtk.MenuButton):
    MENU_MODEL = """
    <?xml version="1.0"?>
        <interface>
        <menu id='app-menu'>
            <section>
                <item>
                    <attribute name='label' translatable='yes'>Preferences</attribute>
                    <attribute name='action'>app.show_preferences</attribute>
                </item>
                <item>
                    <attribute name='label' translatable='yes'>About Photometry</attribute>
                    <attribute name='action'>app.show_about_window</attribute>
                </item>
            </section>
        </menu>
        </interface>
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        builder: Gtk.Builder = Gtk.Builder()
        builder.set_translation_domain("io.github.dlippok.photometric-viewer")
        builder.add_from_string(self.MENU_MODEL)
        menu_model = builder.get_object("app-menu")
        self.set_menu_model(menu_model)
        self.set_icon_name("open-menu-symbolic")
