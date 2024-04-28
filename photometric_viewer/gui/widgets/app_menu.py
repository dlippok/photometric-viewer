import datetime

from gi.repository import Gtk


class ApplicationMenuButton(Gtk.MenuButton):
    MENU_MODEL = """
    <?xml version="1.0"?>
        <interface>
        <menu id='app-menu'>
            <section>
                <item>
                    <attribute name='label' translatable='yes'>New Window</attribute>
                    <attribute name='action'>app.new_window</attribute>
                </item>
            </section>
            <section>
                <item>
                    <attribute name='label' translatable='yes'>Save</attribute>
                    <attribute name='action'>win.save</attribute>
                </item>
                <item>
                    <attribute name='label' translatable='yes'>Save as...</attribute>
                    <attribute name='action'>win.save_as</attribute>
                </item>
                    <submenu>
                        <attribute name='label' translatable='yes'>Export</attribute>
                        <section>
                            <item>
                                <attribute name='label' translatable='yes'>As EULUMDAT</attribute>
                                <attribute name='action'>win.export_as_ldt</attribute>
                            </item>
                            <item>
                                <attribute name='label' translatable='yes'>As IESNA</attribute>
                                <attribute name='action'>win.export_as_ies</attribute>
                            </item>
                            <item>
                                <attribute name='label' translatable='yes'>Light distribution curve</attribute>
                                <attribute name='action'>win.export_ldc_as_image</attribute>
                            </item>
                            <item>
                                <attribute name='label' translatable='yes'>Intensity values</attribute>
                                <attribute name='action'>win.export_intensities_as_csv</attribute>
                            </item>
                            <item>
                                <attribute name='label' translatable='yes'>Luminaire data</attribute>
                                <attribute name='action'>win.export_luminaire_as_json</attribute>
                            </item>
                        </section>
                    </submenu>
            </section>
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
