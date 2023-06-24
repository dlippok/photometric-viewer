from gi.repository import Gtk


class ApplicationMenuButton(Gtk.MenuButton):
    MENU_MODEL = """
    <?xml version="1.0"?>
        <interface>
        <menu id='app-menu'>
            <section>
                <item>
                    <attribute name='label' translatable='yes'>Show source</attribute>
                    <attribute name='action'>app.show_source</attribute>
                </item>
            </section>
            <section>
                <item>
                    <attribute name='label' translatable='yes'>Preferences</attribute>
                    <attribute name='action'>app.show_preferences</attribute>
                </item>
                <item>
                    <attribute name='label' translatable='yes'>About Photometric Viewer</attribute>
                    <attribute name='action'>app.show_about_window</attribute>
                </item>
            </section>
        </menu>
        </interface>
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        builder = Gtk.Builder.new_from_string(self.MENU_MODEL, -1)
        menu_model = builder.get_object("app-menu")
        self.set_menu_model(menu_model)
        self.set_icon_name("open-menu-symbolic")
