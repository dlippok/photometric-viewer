from gi.repository import Gtk, Adw
from gi.repository.Gtk import Label, Orientation, Image

from photometric_viewer.gui.pages.base import BasePage


class EmptyPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(title=_("Empty page"), show_title=False, **kwargs)
        box = Gtk.Box(orientation=Orientation.VERTICAL, valign=Gtk.Align.CENTER, spacing=24)

        app_icon_image: Image = Image().new_from_icon_name("io.github.dlippok.photometric-viewer")
        app_icon_image.set_pixel_size(200)
        box.append(app_icon_image)

        box.append(Label(label=_("Photometry"), css_classes=["title-1"]))
        box.append(Label(label=_("Open photometric file to display it here")))

        buttons_box = Gtk.Box(orientation=Orientation.HORIZONTAL, spacing=10)
        buttons_box.set_halign(Gtk.Align.CENTER)

        buttons_box.append(Gtk.Button(
            label=_("Open File"),
            action_name="app.open",
            css_classes=["suggested-action", "pill"]
        ))

        buttons_box.append(Gtk.Button(
            label=_("New file"),
            action_name="app.new",
            css_classes=["pill"]
        ))

        box.append(buttons_box)

        clamp = Adw.Clamp()
        clamp.set_child(box)

        self.set_content(clamp)
