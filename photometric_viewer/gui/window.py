import io
import logging
from datetime import datetime
from typing import Optional, IO

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
from photometric_viewer.gui.pages.ballast_set import BallastPage
from photometric_viewer.gui.pages.content import PhotometryContentPage
from photometric_viewer.gui.pages.direct_ratios import DirectRatiosPage
from photometric_viewer.gui.pages.empty import EmptyPage
from photometric_viewer.gui.pages.geometry import GeometryPage
from photometric_viewer.gui.pages.lamp_set import LampSetPage
from photometric_viewer.gui.pages.ldc_export import LdcExportPage
from photometric_viewer.gui.pages.photometry import PhotometryPage
from photometric_viewer.gui.pages.source import SourceViewPage
from photometric_viewer.gui.pages.values import IntensityValuesPage
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.gi.GSettings import GSettings
from photometric_viewer.utils.gi.gio import gio_file_stream, write_string
from photometric_viewer.utils.project import PROJECT


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
        self.direct_ratios_page = DirectRatiosPage()
        self.photometry_page = PhotometryPage()
        self.geometry_page = GeometryPage()
        self.lamp_set_page = LampSetPage()
        self.ballast_page = BallastPage()

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

        self.source_view_page.connect("hiding", self.on_hiding_source_page)

        if self.gsettings.settings is None:
            self.show_banner(_("Settings schema could not be loaded. Selected settings will be lost on restart"))

    def show_start_page(self):
        self.navigation_view.replace([self.luminaire_content_page])

    def install_actions(self):
        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)
        self.install_action("app.show_intensity_values", None, self.show_intensity_values)
        self.install_action("app.show_source", None, self.show_source)
        self.install_action("app.show_direct_ratios", None, self.show_direct_ratios)
        self.install_action("app.show_photometry", None, self.show_photometry)
        self.install_action("app.show_geometry", None, self.show_geometry)
        self.install_action("app.show_lamp_set", "i", self.show_lamp_set)
        self.install_action("app.show_ballast", "i", self.show_ballast)
        self.install_action("app.export_luminaire_as_json", None, self.show_json_export_file_chooser)
        self.install_action("app.export_intensities_as_csv", None, self.show_csv_export_file_chooser)
        self.install_action("app.export_ldc_as_image", None, self.show_ldc_export_page)
        self.install_action("app.export_as_ldt", None, self.show_ldt_export_file_chooser)
        self.install_action("app.export_as_ies", None, self.show_ies_export_file_chooser)
        self.install_action("app.open", None, self.on_open_clicked)
        self.install_action("app.open_url", "s", self.on_open_url)


        self.action_set_enabled("app.show_intensity_values", False)
        self.action_set_enabled("app.show_source", False)
        self.action_set_enabled("app.show_direct_ratios", False)
        self.action_set_enabled("app.show_photometry", False)
        self.action_set_enabled("app.show_geometry", False)
        self.action_set_enabled("app.show_lamp_set", False)
        self.action_set_enabled("app.export_luminaire_as_json", False)
        self.action_set_enabled("app.export_intensities_as_csv", False)
        self.action_set_enabled("app.export_ldc_as_image", False)
        self.action_set_enabled("app.export_as_ldt", False)
        self.action_set_enabled("app.export_as_ies", False)
        self.action_set_enabled("app.open_url", True)

    def setup_accelerators(self):
        app = self.get_application()

        for accel in ACCELERATORS:
            app.set_accels_for_action(accel.action, accel.accelerators)

    def display_photometry_content(self, luminaire: Luminaire):
        self.luminaire_content_page.set_photometry(luminaire)
        self.source_view_page.set_photometry(luminaire)
        self.values_table_page.set_photometry(luminaire)
        self.ldc_export_page.set_photometry(luminaire)
        self.direct_ratios_page.set_photometry(luminaire)
        self.photometry_page.set_photometry(luminaire)
        self.geometry_page.set_photometry(luminaire)

        self.opened_photometry = luminaire

    def update_settings(self):
        self.luminaire_content_page.update_settings(self.settings)
        self.lamp_set_page.update_settings(self.settings)
        self.geometry_page.update_settings(self.settings)
        self.gsettings.save(self.settings)

    def on_open_clicked(self, *args):
        self.open_file_chooser.show()

    def on_open_url(self, window, action, params: GLib.Variant, *args):
        Gtk.show_uri(window, params.get_string(), Gdk.CURRENT_TIME)


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
        self.show_start_page()
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
            "_EXPORT_TOOL": PROJECT.name,
            "_EXPORT_TOOL_VERSION": PROJECT.version,
            "_EXPORT_TOOL_HOMEPAGE": PROJECT.urls.homepage,
            "_EXPORT_TOOL_ISSUE_TRACKER": PROJECT.urls.bug_tracker,
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

    def open_stream(self, f: IO):
        photometry = import_from_file(f)

        self.display_photometry_content(photometry)
        self.luminaire_content_page.update_settings(self.settings)
        self.geometry_page.update_settings(self.settings)
        self.lamp_set_page.update_settings(self.settings)

        self.window_title.set_title(_("Photometry"))

        self.action_set_enabled("app.show_intensity_values", True)
        self.action_set_enabled("app.show_source", True)
        self.action_set_enabled("app.show_direct_ratios", True)
        self.action_set_enabled("app.show_photometry", True)
        self.action_set_enabled("app.show_geometry", True)
        self.action_set_enabled("app.show_lamp_set", True)
        self.action_set_enabled("app.export_luminaire_as_json", True)
        self.action_set_enabled("app.export_intensities_as_csv", True)
        self.action_set_enabled("app.export_ldc_as_image", True)
        self.action_set_enabled("app.export_as_ldt", True)
        self.action_set_enabled("app.export_as_ies", True)

        self.show_start_page()



    def open_file(self, file: Gio.File):
        try:
            with gio_file_stream(file) as f:
                filename = file.get_basename()
                self.open_stream(f)
                self.set_title(title=filename)
                self.window_title.set_subtitle(filename)
                self.json_export_file_chooser.set_current_name(f"{filename}.json")
                self.csv_export_file_chooser.set_current_name(f"{filename}.csv")
                self.ldt_export_file_chooser.set_current_name(f"{filename}_exported.ldt")
                self.ies_export_file_chooser.set_current_name(f"{filename}_exported.ies")

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

    def show_direct_ratios(self, *args):
        self.navigation_view.push(self.direct_ratios_page)

    def show_photometry(self, *args):
        self.navigation_view.push(self.photometry_page)

    def show_geometry(self, *args):
        self.navigation_view.push(self.geometry_page)

    def show_lamp_set(self, window, action, params: GLib.Variant, *args):
        if self.opened_photometry is None:
            return

        lamp_index = params.get_int32()
        if len(self.opened_photometry.lamps) < lamp_index:
            return

        lamp_set = self.opened_photometry.lamps[lamp_index]

        self.lamp_set_page.set_lamp_set(self.opened_photometry, lamp_set)
        self.navigation_view.push(self.lamp_set_page)

    def show_ballast(self, window, action, params: GLib.Variant, *args):
        if self.opened_photometry is None:
            return

        lamp_index = params.get_int32()
        if len(self.opened_photometry.lamps) < lamp_index:
            return

        lamp_set = self.opened_photometry.lamps[lamp_index]

        self.ballast_page.set_lamp_set(lamp_set)
        self.navigation_view.push(self.ballast_page)

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

    def on_hiding_source_page(self, source_view_page: SourceViewPage):
        buffer: Gtk.TextBuffer = source_view_page.source_text_view.get_buffer()
        start = buffer.get_start_iter()
        end = buffer.get_end_iter()

        self.open_stream(
            io.StringIO(buffer.get_text(start, end, True))
        )


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
