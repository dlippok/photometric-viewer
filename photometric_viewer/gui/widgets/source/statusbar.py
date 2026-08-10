from gi.repository import Gtk
from gi.repository.GtkSource import Language


class StatusBar(Gtk.Box):
    def __init__(self):
        super().__init__(
            orientation=Gtk.Orientation.HORIZONTAL,
            css_classes=["statusbar"]
        )

        self.language_label = Gtk.Label(margin_start=6, margin_end=6, margin_top=6, margin_bottom=6)

        self.append(Gtk.Separator())
        self.append(Gtk.Image(icon_name="text-editor-symbolic", margin_start=12))
        self.append(self.language_label)
        self.append(Gtk.Separator())

        self.set_source_language(None)

    def set_source_language(self, lang: Language | None):
        if lang:
            self.language_label.set_label(lang.get_name())
        else:
            self.language_label.set_label(_("Unknown"))

