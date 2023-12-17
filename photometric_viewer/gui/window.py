import io
import logging
from datetime import datetime
from typing import Optional

from gi.repository import Adw, Gtk, Gio, GLib, Gdk
from gi.repository.Gtk import FileChooserDialog, DropTarget

import photometric_viewer.formats.csv
import photometric_viewer.formats.format_json
import photometric_viewer.formats.png
import photometric_viewer.formats.svg
from photometric_viewer.config.accelerators import ACCELERATORS
from photometric_viewer.formats import ldt, ies
from photometric_viewer.formats.common import import_from_file
from photometric_viewer.formats.exceptions import InvalidPhotometricFileFormatException
from photometric_viewer.gui.dialogs.about import AboutWindow
from photometric_viewer.gui.dialogs.file_chooser import OpenFileChooser, ExportFileChooser
from photometric_viewer.gui.dialogs.preferences import PreferencesWindow
from photometric_viewer.gui.pages.content import PhotometryContentPage
from photometric_viewer.gui.pages.empty import EmptyPage
from photometric_viewer.gui.pages.ldc_export import LdcExportPage
from photometric_viewer.gui.pages.source import SourceViewPage
from photometric_viewer.gui.pages.values import IntensityValuesPage
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.gi.GSettings import GSettings
from photometric_viewer.utils.gi.gio import gio_file_stream, write_string


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(
            title=_('Photometry'),
            **kwargs
        )

        self.set_default_size(900, 700)
        self.install_actions()
        self.setup_accelerators()

        self.gsettings = GSettings()

        self.settings = self.gsettings.load()

        self.navigation_view = Adw.NavigationView()

        self.opened_photometry: Optional[Luminaire] = None

        self.luminaire_content_page = PhotometryContentPage()
        self.source_view_page = SourceViewPage()
        self.values_table_page = IntensityValuesPage()
        self.ldc_export_page = LdcExportPage(on_exported=self.on_export_ldc_response, transient_for=self)

        empty_page = EmptyPage()
        self.navigation_view.replace([empty_page])

        self.toast_overlay = Adw.ToastOverlay()
        self.toast_overlay.set_child(self.navigation_view)

        self.window_title = Adw.WindowTitle()

        self.open_file_chooser = OpenFileChooser(transient_for=self)
        self.open_file_chooser.connect("response", self.on_open_response)

        self.json_export_file_chooser = ExportFileChooser.for_json(transient_for=self)
        self.json_export_file_chooser.connect("response", self.on_export_json_response)

        self.csv_export_file_chooser = ExportFileChooser.for_csv(transient_for=self)
        self.csv_export_file_chooser.connect("response", self.on_export_csv_response)

        self.ldt_export_file_chooser = ExportFileChooser.for_ldt(transient_for=self)
        self.ldt_export_file_chooser.connect("response", self.on_export_ldt_response)

        self.ies_export_file_chooser = ExportFileChooser.for_ies(transient_for=self)
        self.ies_export_file_chooser.connect("response", self.on_export_ies_response)

        self.set_content(self.toast_overlay)

        self.drop_target = DropTarget(
            actions=Gdk.DragAction.COPY
        )
        self.drop_target.set_gtypes([Gio.File])

        self.drop_target.connect("drop", self.on_drop)
        self.add_controller(self.drop_target)

        if self.gsettings.settings is None:
            self.show_banner(_("Settings schema could not be loaded. Selected settings will be lost on restart"))

    def show_start_page(self):
        self.navigation_view.replace([self.luminaire_content_page])

    def install_actions(self):
        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)
        self.install_action("app.show_intensity_values", None, self.show_intensity_values)
        self.install_action("app.show_source", None, self.show_source)
        self.install_action("app.export_luminaire_as_json", None, self.show_json_export_file_chooser)
        self.install_action("app.export_intensities_as_csv", None, self.show_csv_export_file_chooser)
        self.install_action("app.export_ldc_as_image", None, self.show_ldc_export_page)
        self.install_action("app.export_as_ldt", None, self.show_ldt_export_file_chooser)
        self.install_action("app.export_as_ies", None, self.show_ies_export_file_chooser)
        self.install_action("app.open", None, self.on_open_clicked)


        self.action_set_enabled("app.show_intensity_values", False)
        self.action_set_enabled("app.show_source", False)
        self.action_set_enabled("app.export_luminaire_as_json", False)
        self.action_set_enabled("app.export_intensities_as_csv", False)
        self.action_set_enabled("app.export_ldc_as_image", False)
        self.action_set_enabled("app.export_as_ldt", False)
        self.action_set_enabled("app.export_as_ies", False)

    def setup_accelerators(self):
        app = self.get_application()

        for accel in ACCELERATORS:
            app.set_accels_for_action(accel.action, accel.accelerators)

    def display_photometry_content(self, luminaire: Luminaire):
        self.luminaire_content_page.set_photometry(luminaire)
        self.source_view_page.set_photometry(luminaire)
        self.values_table_page.set_photometry(luminaire)
        self.ldc_export_page.set_photometry(luminaire)

        self.opened_photometry = luminaire

    def update_settings(self):
        self.luminaire_content_page.update_settings(self.settings)
        self.gsettings.save(self.settings)

    def on_open_clicked(self, *args):
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
        data = photometric_viewer.formats.format_json.export_photometry(self.opened_photometry)
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

    def on_export_ldc_response(self, filename):
        self.open_page(self.luminaire_content_page)
        self.show_banner(_("Exported as {}").format(filename))

    def on_export_ldt_response(self, dialog: FileChooserDialog, response):
        if not self.opened_photometry:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()

        with io.StringIO() as f:
            ldt.export_to_file(f, self.opened_photometry)
            write_string(file, f.getvalue())
        self.show_banner(_("Exported as {}").format(file.get_basename()))

    def on_export_ies_response(self, dialog: FileChooserDialog, response):
        if not self.opened_photometry:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()

        export_keywords = {
            "_EXPORT_TOOL": _("Photometry"),
            "_EXPORT_TOOL_VERSION": "1.3.0",
            "_EXPORT_TOOL_URL": "https://github.com/dlippok/photometric-viewer",
            "_EXPORT_TOOL_ISSUE_TRACKER": "https://github.com/dlippok/photometric-viewer/issues",
            "_EXPORT_TIMESTAMP": datetime.now().isoformat()
        }

        with io.StringIO() as f:
            ies.export_to_file(f, self.opened_photometry, export_keywords)
            write_string(file, f.getvalue())
        self.show_banner(_("Exported as {}").format(file.get_basename()))

    def on_title_visible_changed(self, *args):
        title_visible = self.window_title.get_title_visible()
        self.switcher_bar.set_reveal(title_visible)

    def on_drop(self, target, file, *args):
        self.open_file(file)
        return True


    def open_file(self, file: Gio.File):
        try:
            with gio_file_stream(file) as f:
                photometry = import_from_file(f)

                self.display_photometry_content(photometry)
                self.luminaire_content_page.update_settings(self.settings)

                self.set_title(title=file.get_basename())
                self.window_title.set_title(_("Photometry"))
                self.window_title.set_subtitle(file.get_basename())

                self.action_set_enabled("app.show_intensity_values", True)
                self.action_set_enabled("app.show_source", True)
                self.action_set_enabled("app.export_luminaire_as_json", True)
                self.action_set_enabled("app.export_intensities_as_csv", True)
                self.action_set_enabled("app.export_ldc_as_image", True)
                self.action_set_enabled("app.export_as_ldt", True)
                self.action_set_enabled("app.export_as_ies", True)

                opened_filename = file.get_basename()
                self.json_export_file_chooser.set_current_name(f"{opened_filename}.json")
                self.csv_export_file_chooser.set_current_name(f"{opened_filename}.csv")
                self.ldt_export_file_chooser.set_current_name(f"{opened_filename}_exported.ldt")
                self.ies_export_file_chooser.set_current_name(f"{opened_filename}_exported.ies")
                self.show_start_page()

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
        self.navigation_view.push(self.source_view_page)

    def show_intensity_values(self, *args):
        self.navigation_view.push(self.values_table_page)

    def show_json_export_file_chooser(self, *args):
        self.json_export_file_chooser.show()

    def show_csv_export_file_chooser(self, *args):
        self.csv_export_file_chooser.show()

    def show_ldc_export_file_chooser(self, *args):
        self.ldc_export_file_chooser.show()

    def show_ldt_export_file_chooser(self, *args):
        self.ldt_export_file_chooser.show()

    def show_ies_export_file_chooser(self, *args):
        self.ies_export_file_chooser.show()

    def show_ldc_export_page(self, *args):
        self.navigation_view.push(self.ldc_export_page)

    def show_banner(self, message: str, details: str | None = None):
        toast = Adw.Toast()
        toast.set_timeout(3)
        if details:
            toast.set_title(f"{message}\n{details}")
        else:
            toast.set_title(message)
        self.toast_overlay.add_toast(toast)

    @staticmethod
    def show_about_dialog(*args):
        window = AboutWindow()
        window.show()
