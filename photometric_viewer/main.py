import os

import gi


gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from photometric_viewer.utils.locales import init_locale
from photometric_viewer.gui.window import MainWindow
from gi.repository import Gio, Adw, Gtk, Gdk
import sys


APPLICATION_ID = 'io.github.dlippok.photometric-viewer'
init_locale(APPLICATION_ID)


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID,
                         flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.NON_UNIQUE)
        self.win = None

    def create_window(self):
        self.win = MainWindow(application=self)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.dirname(__file__) + "/styles/style.css")

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def do_startup(self):
        Adw.Application.do_startup(self)
        self.create_window()

    def do_activate(self):
        self.props.active_window.present()

    def do_shutdown(self):
        Adw.Application.do_shutdown(self)

    def do_open(self, *args, **kwargs):
        file: Gio.File = args[0][0]
        self.win.open_file(file)
        self.props.active_window.present()


def run():
    app = Application()
    app.run(sys.argv)
