import os

import gi

from photometric_viewer.config.accelerators import ACCELERATORS
from photometric_viewer.utils.project import ASSETS_PATH

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')
gi.require_version(namespace='GtkSource', version='5')

from photometric_viewer.utils.locales import init_locale
from photometric_viewer.gui.window import MainWindow
from gi.repository import Gio, Adw, Gtk, Gdk
import sys


APPLICATION_ID = 'io.github.dlippok.photometric-viewer'
init_locale(APPLICATION_ID)

theme: Gtk.IconTheme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
theme.add_search_path(os.path.join(ASSETS_PATH, "icons"))

class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id=APPLICATION_ID,
                         flags=Gio.ApplicationFlags.HANDLES_OPEN | Gio.ApplicationFlags.NON_UNIQUE)

    def do_startup(self):
        Adw.Application.do_startup(self)

    def new_window(self):
        window = MainWindow()
        self.add_window(window)
        window.present()
        return window

    def do_activate(self):
        self.setup_css()
        self.setup_accelerators()
        self.new_window()

    def do_shutdown(self):
        Adw.Application.do_shutdown(self)

    def do_open(self, *args, **kwargs):
        file: Gio.File = args[0][0]
        window = self.new_window()
        window.open_file(file)

    def setup_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(os.path.dirname(__file__) + "/assets/style.css")

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def setup_accelerators(self):
        for accel in ACCELERATORS:
            self.set_accels_for_action(accel.action, accel.accelerators)


def run():
    app = Application()
    app.run(sys.argv)
