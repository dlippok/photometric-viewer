from gi.repository import Adw, Gtk
from gi.repository.Gtk import Orientation

from photometric_viewer.gui.widgets.headerbar import default_headerbar


class BasePage(Adw.NavigationPage):
    def __init__(self, title, show_title=True, headerbar=None, content=None, **kwargs):
        super().__init__(title=title, **kwargs)
        self.content_bin = Adw.Bin(hexpand=True, vexpand=True)

        header = headerbar or default_headerbar()

        header.set_show_title(show_title)

        if content:
            self.content_bin.set_child(content)

        content_box = Gtk.Box(orientation=Orientation.VERTICAL)

        content_box.append(header)
        content_box.append(self.content_bin)

        self.set_child(content_box)

    def set_content(self, content):
        self.content_bin.set_child(content)

