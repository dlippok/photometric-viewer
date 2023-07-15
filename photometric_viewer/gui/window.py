import logging
from typing import Optional

from gi.repository import Adw, Gtk, Gio, GLib
from gi.repository.Adw import ViewStackPage
from gi.repository.Gtk import Orientation, Button, FileChooserDialog

import photometric_viewer.formats.csv
import photometric_viewer.formats.format_json
import photometric_viewer.formats.png
import photometric_viewer.formats.svg
from photometric_viewer.formats.common import import_from_file
from photometric_viewer.formats.exceptions import InvalidPhotometricFileFormatException
from photometric_viewer.gui.dialogs.about import AboutWindow
from photometric_viewer.gui.dialogs.file_chooser import OpenFileChooser, ExportFileChooser
from photometric_viewer.gui.dialogs.preferences import PreferencesWindow
from photometric_viewer.gui.pages.content import PhotometryContent
from photometric_viewer.gui.pages.empty import EmptyPage
from photometric_viewer.gui.pages.source import SourceView
from photometric_viewer.gui.pages.values import IntensityValues
from photometric_viewer.gui.widgets.app_menu import ApplicationMenuButton
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.GSettings import GSettings
from photometric_viewer.utils.gio import gio_file_stream, write_string, write_bytes


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(
            title='Photometric Viewer',
            **kwargs
        )
        self.set_default_size(900, 700)
        self.install_actions()

        self.gsettings = GSettings()
        if self.gsettings.settings is None:
            self.show_banner(_("Settings schema could not be loaded. Selected settings will be lost on restart"))

        self.settings = self.gsettings.load()

        self.view_stack = Adw.ViewStack()
        self.opened_photometry: Optional[Photometry] = None
        self.opened_filename: str | None = None

        self.photometry_content = PhotometryContent()
        properties_page: ViewStackPage = self.view_stack.add_titled(self.photometry_content, "photometry", _("Photometry"))
        properties_page.set_icon_name("view-reveal-symbolic")

        self.source_view = SourceView()
        source_page: ViewStackPage = self.view_stack.add_titled(self.source_view, "source", _("Source"))
        source_page.set_icon_name("view-paged-symbolic")
        source_page.set_visible(False)

        self.values_table = IntensityValues()
        values_page: ViewStackPage = self.view_stack.add_titled(self.values_table, "values", _("Intensity Values"))
        values_page.set_icon_name("view-grid-symbolic")

        self.content_bin = Adw.Bin()
        self.content_bin.set_child(EmptyPage())
        self.content_bin.set_vexpand(True)

        self.banner = Adw.Banner()
        self.banner.set_button_label(_("Dismiss"))
        self.banner.connect("button-clicked", self.banner_dismiss_clicked)

        open_button = Button(
            child=Adw.ButtonContent(label=_("Open"), icon_name="document-open-symbolic")
        )

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

        self.open_file_chooser = OpenFileChooser(transient_for=self)
        self.open_file_chooser.connect("response", self.on_open_response)

        self.json_export_file_chooser = ExportFileChooser.for_json(transient_for=self)
        self.json_export_file_chooser.connect("response", self.on_export_json_response)

        self.csv_export_file_chooser = ExportFileChooser.for_csv(transient_for=self)
        self.csv_export_file_chooser.connect("response", self.on_export_csv_response)

        self.ldc_export_file_chooser = ExportFileChooser.for_ldc(transient_for=self)
        self.ldc_export_file_chooser.connect("response", self.on_export_ldc_response)

        self.set_content(box)

    def install_actions(self):
        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)
        self.install_action("app.show_source", None, self.show_source)
        self.install_action("app.export_luminaire_as_json", None, self.show_json_export_file_chooser)
        self.install_action("app.export_intensities_as_csv", None, self.show_csv_export_file_chooser)
        self.install_action("app.export_ldc_as_image", None, self.show_ldc_export_file_chooser)
        self.action_set_enabled("app.show_source", False)
        self.action_set_enabled("app.export_luminaire_as_json", False)
        self.action_set_enabled("app.export_intensities_as_csv", False)
        self.action_set_enabled("app.export_ldc_as_image", False)

    def display_photometry_content(self, photometry: Photometry):
        self.photometry_content.set_photometry(photometry)
        self.source_view.set_photometry(photometry)
        self.values_table.set_photometry(photometry)

        self.content_bin.set_child(self.view_stack)
        self.switcher_bar.set_stack(self.view_stack)
        self.opened_photometry = photometry
        self.action_set_enabled("app.show_source", True)
        self.action_set_enabled("app.export_luminaire_as_json", True)
        self.action_set_enabled("app.export_intensities_as_csv", True)
        self.action_set_enabled("app.export_ldc_as_image", True)

    def update_settings(self):
        self.photometry_content.update_settings(self.settings)
        self.gsettings.save(self.settings)

    def on_open_clicked(self, _):
        self.open_file_chooser.show()

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            self.open_file(file)

    def on_export_json_response(self, dialog: FileChooserDialog, response):
        if not self.opened_photometry:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()
        data = photometric_viewer.formats.json.export_photometry(self.opened_photometry)
        write_string(file, data)
        self.show_banner(_("Exported as {}").format(file.get_basename()))

    def on_export_csv_response(self, dialog: FileChooserDialog, response):
        if not self.opened_photometry:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()
        data = photometric_viewer.formats.csv.export_photometry(self.opened_photometry)
        write_string(file, data)
        self.show_banner(_("Exported as {}").format(file.get_basename()))

    def on_export_ldc_response(self, dialog: FileChooserDialog, response):
        if not self.opened_photometry:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()
        if file.get_basename().endswith(".svg"):
            data = photometric_viewer.formats.svg.export_photometry(self.opened_photometry)
        else:
            data = photometric_viewer.formats.png.export_photometry(self.opened_photometry)
        write_bytes(file, data)
        self.show_banner(_("Exported as {}").format(file.get_basename()))

    def open_file(self, file: Gio.File):
        self.banner.set_revealed(False)
        try:
            with gio_file_stream(file) as f:
                photometry = import_from_file(f)
                if photometry.metadata.luminaire:
                    self.set_title(title=photometry.metadata.luminaire)
                self.display_photometry_content(photometry)
                self.photometry_content.update_settings(self.settings)
                self.opened_filename = file.get_basename()
        except GLib.GError as e:
            logging.exception("Could not open photometric file")
            self.show_banner(e.message)
        except InvalidPhotometricFileFormatException as e:
            logging.exception("Could not open photometric file")
            self.show_banner(_("Invalid content of photometric file {}").format(file.get_path()), str(e))
        except Exception:
            logging.exception("Could not open photometric file")
            self.show_banner(_("Could not open {}").format(file.get_path()))

    def show_preferences(self, *args):
        window = PreferencesWindow(self.settings, self.update_settings)
        window.show()

    def show_source(self, *args):
        self.view_stack.set_visible_child(self.source_view)

    def show_json_export_file_chooser(self, *args):
        if not self.json_export_file_chooser.get_current_name():
            self.json_export_file_chooser.set_current_name(f"{self.opened_filename}.json")
        self.json_export_file_chooser.show()

    def show_csv_export_file_chooser(self, *args):
        if not self.csv_export_file_chooser.get_current_name():
            self.csv_export_file_chooser.set_current_name(f"{self.opened_filename}.csv")
        self.csv_export_file_chooser.show()

    def show_ldc_export_file_chooser(self, *args):
        if not self.ldc_export_file_chooser.get_current_name():
            self.ldc_export_file_chooser.set_current_name(f"{self.opened_filename}.png")
        self.ldc_export_file_chooser.show()

    def banner_dismiss_clicked(self, *args):
        self.banner.set_revealed(False)

    def show_banner(self, message: str, details: str | None = None):
        if details:
            self.banner.set_title(f"{message}\n{details}")
        else:
            self.banner.set_title(message)
        self.banner.set_revealed(True)

    @staticmethod
    def show_about_dialog(*args):
        window = AboutWindow()
        window.show()
