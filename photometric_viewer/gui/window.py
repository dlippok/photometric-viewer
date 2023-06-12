import logging
from typing import Optional

from gi.repository import Adw, Gtk, Gio, GLib
from gi.repository.Adw import ViewStackPage
from gi.repository.Gtk import Orientation, Button, FileChooserDialog, FileFilter, FileChooserNative

from photometric_viewer.formats.common import import_from_file
from photometric_viewer.formats.exceptions import InvalidPhotometricFileFormatException
from photometric_viewer.gui.about import AboutWindow
from photometric_viewer.gui.content import PhotometryContent
from photometric_viewer.gui.empty import EmptyPage
from photometric_viewer.gui.menu import ApplicationMenuButton
from photometric_viewer.gui.settings.settings import PreferencesWindow
from photometric_viewer.gui.source import SourceView
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.GSettings import GSettings
from photometric_viewer.utils.gio import gio_file_stream


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.gsettings = GSettings()
        if self.gsettings.settings == None:
            self.show_error("Settings schema could not be loaded. Selected settings will be lost on restart")

        self.settings = self.gsettings.load()
        self.opened_photometry: Optional[Photometry] = None
        self.photometry_content = PhotometryContent()

        self.set_default_size(550, 700)
        self.set_title(title='Photometric Viewer')

        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)

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

        photometric_filter = FileFilter(name="All photometric files")
        photometric_filter.add_pattern("*.ies")
        photometric_filter.add_pattern("*.ldt")

        ies_filter = FileFilter(name="IESNA (*.ies)")
        ies_filter.add_pattern("*.ies")

        ldt_filter = FileFilter(name="EULUMDAT (*.ldt)")
        ldt_filter.add_pattern("*.ldt")

        all_files_filter = FileFilter(name="All Files")
        all_files_filter.add_pattern("*")

        self.file_chooser = FileChooserNative(
            action=Gtk.FileChooserAction.OPEN,
            select_multiple=False,
            modal=True,
            transient_for=self
        )
        self.file_chooser.connect("response", self.on_open_response)
        self.file_chooser.add_filter(photometric_filter)
        self.file_chooser.add_filter(ies_filter)
        self.file_chooser.add_filter(ldt_filter)
        self.file_chooser.add_filter(all_files_filter)

        self.set_content(box)

    def display_photometry_content(self, photometry: Photometry):
        self.photometry_content = PhotometryContent()
        self.photometry_content.set_photometry(photometry)

        source_view = SourceView()
        source_view.set_photometry(photometry)

        view_stack = Adw.ViewStack()

        properties_page: ViewStackPage = view_stack.add_titled(self.photometry_content, "photometry", "Photometry")
        properties_page.set_icon_name("view-reveal-symbolic")

        source_page: ViewStackPage = view_stack.add_titled(source_view, "source", "Source")
        source_page.set_icon_name("view-paged-symbolic")

        self.content_bin.set_child(view_stack)
        self.switcher_bar.set_stack(view_stack)
        self.opened_photometry = photometry

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
