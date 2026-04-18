from gi.repository import Gtk, Adw
from gi.repository.Gtk import Orientation, PolicyType, ScrolledWindow, Align

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.headerbar import default_headerbar


class EmptyContentPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__("", headerbar=default_headerbar(), **kwargs)
        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
            valign=Align.CENTER
        )


        box.append(Gtk.Image(icon_name="io.github.dlippok.photometric-viewer", pixel_size=128))
        box.append(Gtk.Label(label=_('Photometry'), css_classes=['title-1']))
        box.append(Gtk.Label(label=_('Open photometric file to display it here'), wrap=True))

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)
