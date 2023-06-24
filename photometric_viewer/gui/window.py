import logging
from typing import Optional

from gi.repository import Adw, Gtk, Gio, GLib
from gi.repository.Adw import ViewStackPage
from gi.repository.Gtk import Orientation, Button, FileChooserDialog

from photometric_viewer.formats.common import import_from_file
from photometric_viewer.formats.exceptions import InvalidPhotometricFileFormatException
from photometric_viewer.gui.dialogs.about import AboutWindow
from photometric_viewer.gui.dialogs.file_chooser import FileChooser
from photometric_viewer.gui.dialogs.preferences import PreferencesWindow
from photometric_viewer.gui.pages.content import PhotometryContent
from photometric_viewer.gui.pages.empty import EmptyPage
from photometric_viewer.gui.pages.source import SourceView
from photometric_viewer.gui.pages.values import IntensityValues
from photometric_viewer.gui.widgets.app_menu import ApplicationMenuButton
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.GSettings import GSettings
from photometric_viewer.utils.gio import gio_file_stream


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(
            title='Photometric Viewer',
            **kwargs
        )
        self.set_default_size(550, 700)
        self.install_actions()

        self.gsettings = GSettings()
        if self.gsettings.settings is None:
            self.show_error("Settings schema could not be loaded. Selected settings will be lost on restart")

        self.settings = self.gsettings.load()

        self.view_stack = Adw.ViewStack()
        self.opened_photometry: Optional[Photometry] = None

        self.photometry_content = PhotometryContent()
        properties_page: ViewStackPage = self.view_stack.add_titled(self.photometry_content, "photometry", "Photometry")
        properties_page.set_icon_name("view-reveal-symbolic")

        self.source_view = SourceView()
        source_page: ViewStackPage = self.view_stack.add_titled(self.source_view, "source", "Source")
        source_page.set_icon_name("view-paged-symbolic")
        source_page.set_visible(False)

        self.values_table = IntensityValues()
        values_page: ViewStackPage = self.view_stack.add_titled(self.values_table, "values", "Intensity Values")
        values_page.set_icon_name("view-grid-symbolic")

        self.content_bin = Adw.Bin()
        self.content_bin.set_child(EmptyPage())
        self.content_bin.set_vexpand(True)

        self.banner = Adw.Banner()
        self.banner.set_button_label("Dismiss")
        self.banner.connect("button-clicked", self.banner_dismiss_clicked)

        open_button = Button(label="Open")
        open_button.connect("clicked", self.on_open_clicked)

        self.switcher_bar = Adw.ViewSwitcherTitle()
        self.switcher_bar.set_title("Photometric Viewer")
        self.switcher_bar.set_visible(True)

        box = Gtk.Box(orientation=Orientation.VERTICAL)
        header_bar = Adw.HeaderBar()
        header_bar.set_title_widget(self.switcher_bar)
        header_bar.pack_start(open_button)
        header_bar.pack_end(ApplicationMenuButton())
        box.append(header_bar)
        box.append(self.banner)
        box.append(self.content_bin)

        self.file_chooser = FileChooser(transient_for=self)
        self.file_chooser.connect("response", self.on_open_response)

        self.set_content(box)

    def install_actions(self):
        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)
        self.install_action("app.show_source", None, self.show_source)
        self.action_set_enabled("app.show_source", False)

    def display_photometry_content(self, photometry: Photometry):
        self.photometry_content.set_photometry(photometry)
        self.source_view.set_photometry(photometry)
        self.values_table.set_photometry(photometry)

        self.content_bin.set_child(self.view_stack)
        self.switcher_bar.set_stack(self.view_stack)
        self.opened_photometry = photometry
        self.action_set_enabled("app.show_source", True)

    def update_settings(self):
        self.photometry_content.update_settings(self.settings)
        self.gsettings.save(self.settings)

    def on_open_clicked(self, _):
        self.file_chooser.show()

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            self.open_file(file)

    def open_file(self, file: Gio.File):
        self.banner.set_revealed(False)
        try:
            with gio_file_stream(file) as f:
                photometry = import_from_file(f)
                if photometry.metadata.luminaire:
                    self.set_title(title=photometry.metadata.luminaire)
                self.display_photometry_content(photometry)
                self.photometry_content.update_settings(self.settings)
        except GLib.GError as e:
            logging.exception("Could not open photometric file")
            self.show_error(e.message)
        except InvalidPhotometricFileFormatException as e:
            logging.exception("Could not open photometric file")
            self.show_error(f"Invalid content of photometric file {file.get_path()}", str(e))
        except Exception:
            logging.exception("Could not open photometric file")
            self.show_error(f"Could not open {file.get_path()}")

    def show_preferences(self, *args):
        window = PreferencesWindow(self.settings, self.update_settings)
        window.show()

    def show_source(self, *args):
        self.view_stack.set_visible_child(self.source_view)

    def banner_dismiss_clicked(self, *args):
        self.banner.set_revealed(False)

    def show_error(self, message: str, details: str | None = None):
        if details:
            self.banner.set_title(f"{message}\n{details}")
        else:
            self.banner.set_title(message)
        self.banner.set_revealed(True)

    @staticmethod
    def show_about_dialog(*args):
        window = AboutWindow()
        window.show()
