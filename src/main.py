import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gui.window import MainWindow
from gi.repository import Gio, Adw, Gtk, Gdk
import sys


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='adw.flap.demo',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.win = None

    def do_startup(self):
        Adw.Application.do_startup(self)

    def do_activate(self):
        self.win = self.props.active_window
        if not self.win:
            self.win = MainWindow(application=self)
        self.win.present()
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path("style.css")

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_shutdown(self):
        Adw.Application.do_shutdown(self)


if __name__ == '__main__':


    app = Application()
    app.run(sys.argv)
