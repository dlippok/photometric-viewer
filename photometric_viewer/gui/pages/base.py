from gi.repository import Adw, Gtk
from gi.repository.Gtk import Orientation, ScrolledWindow, Box, PolicyType

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH


class BasePage(Adw.NavigationPage):
    def __init__(self, title, show_title=True, headerbar=None, content=None, **kwargs):
        super().__init__(title=title, **kwargs)
        self.content_bin = Adw.Bin(hexpand=True, vexpand=True)

        header = headerbar or Adw.HeaderBar(css_classes=["flat"])

        header.set_show_title(show_title)

        if content:
            self.content_bin.set_child(content)

        content_box = Gtk.Box(orientation=Orientation.VERTICAL)

        content_box.append(header)
        content_box.append(self.content_bin)

        self.set_child(content_box)

    def set_content(self, content):
        self.content_bin.set_child(content)


class SidebarPage(BasePage):
    def __init__(self, title, show_title=True, headerbar=None, content=None, **kwargs):
        super().__init__(title=title, **kwargs)

        self._box = Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16,
        )

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(self._box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        super().set_content(scrolled_window)


    def append(self, content):
        self._box.append(content)