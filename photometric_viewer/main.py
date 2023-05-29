import os

import gi

from photometric_viewer.formats.ies import import_from_file
from photometric_viewer.utils.gio import gio_file_stream

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from photometric_viewer.gui.window import MainWindow
from gi.repository import Gio, Adw, Gtk, Gdk
import sys


class Application(Adw.Application):
    def __init__(self):
        super().__init__(application_id='io.github.dlippok.photometric-viewer',
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
        with gio_file_stream(file) as f:
            photometry = import_from_file(f)
            self.win.open_photometry(photometry)
        self.props.active_window.present()

def run():
    app = Application()
    app.run(sys.argv)