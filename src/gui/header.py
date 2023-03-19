from gi.repository import Gtk


class Header(Gtk.Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["h1"])
