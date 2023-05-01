from gi.repository import Gtk, Adw
from gi.repository.Gtk import Label, Orientation


class EmptyPage(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = Gtk.Box(orientation=Orientation.VERTICAL, valign=Gtk.Align.CENTER, spacing=15)

        box.append(Label(label="No content", name="no-content-header"))
        box.append(Label(label="Open photometric file to display it here", name="no-content-subtitle"))

        clamp = Adw.Clamp()
        clamp.set_child(box)

        self.set_child(clamp)