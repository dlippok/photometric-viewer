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
from photometric_viewer.formats import ldt, ies
from photometric_viewer.formats.common import import_from_file
from photometric_viewer.formats.exceptions import InvalidPhotometricFileFormatException
from photometric_viewer.gui.dialogs.about import AboutWindow
from photometric_viewer.gui.dialogs.file_chooser import ExportFileChooser, FileChooser
from photometric_viewer.gui.dialogs.preferences import PreferencesWindow
from photometric_viewer.gui.pages.ballast_set import BallastPage
from photometric_viewer.gui.pages.content import PhotometryContentPage
from photometric_viewer.gui.pages.direct_ratios import DirectRatiosPage
from photometric_viewer.gui.pages.geometry import GeometryPage
from photometric_viewer.gui.pages.lamp_set import LampSetPage
from photometric_viewer.gui.pages.ldc_export import LdcExportPage
from photometric_viewer.gui.pages.ldc_zoom import LdcZoomPage
from photometric_viewer.gui.pages.photometry import PhotometryPage
from photometric_viewer.gui.pages.photometry_export import PhotometryExportPage
from photometric_viewer.gui.pages.source import SourceViewPage
from photometric_viewer.gui.pages.values import IntensityValuesPage
from photometric_viewer.gui.widgets.common.split_view import SplitView
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.gi.GSettings import SettingsManager
from photometric_viewer.utils.gi.gio import gio_file_stream, write_string
from photometric_viewer.utils.project import PROJECT


class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(
            title=_('Photometry'),
            **kwargs
        )

        self.is_opening = False
        self.pending_action = None
        self.is_dirty = False

        self.set_default_size(1000, 700)
        self.install_actions()

        self.settings_manager = SettingsManager()

        self.navigation_view = Adw.NavigationView()

        self.opened_photometry: Optional[Luminaire] = None
        self.opened_file: Gio.File | None = None

        self.luminaire_content_page = PhotometryContentPage()
        self.source_view_page = SourceViewPage()
        self.values_table_page = IntensityValuesPage()
        self.ldc_export_page = LdcExportPage(on_exported=self.on_export_response, transient_for=self)
        self.photometry_export_page = PhotometryExportPage(on_exported=self.on_export_response, transient_for=self)
        self.direct_ratios_page = DirectRatiosPage()
        self.photometry_page = PhotometryPage()
        self.geometry_page = GeometryPage()
        self.lamp_set_page = LampSetPage()
        self.ballast_page = BallastPage()
        self.ldc_zoom_page = LdcZoomPage()

        self.navigation_view.replace([self.luminaire_content_page])
        self.on_new()

        self.toast_overlay = Adw.ToastOverlay()
        overlay_split_view = SplitView(
            navigation_view=self.navigation_view,
            source_view_page=self.source_view_page
        )

        self.toast_overlay.set_child(overlay_split_view)

        self.window_title = Adw.WindowTitle()

        self.open_file_chooser = FileChooser(transient_for=self, action=Gtk.FileChooserAction.OPEN)
        self.open_file_chooser.connect("response", self.on_open_response)

        self.save_as_file_chooser = FileChooser(transient_for=self, action=Gtk.FileChooserAction.SAVE)
        self.save_as_file_chooser.connect("response", self.on_save_as_response)

        self.json_export_file_chooser = ExportFileChooser.for_json(transient_for=self)
        self.json_export_file_chooser.connect("response", self.on_export_json_response)

        self.csv_export_file_chooser = ExportFileChooser.for_csv(transient_for=self)
        self.csv_export_file_chooser.connect("response", self.on_export_csv_response)

        self.set_content(self.toast_overlay)

        self.drop_target = DropTarget(
            actions=Gdk.DragAction.COPY
        )
        self.drop_target.set_gtypes([Gio.File])

        self.drop_target.connect("drop", self.on_drop)
        self.add_controller(self.drop_target)

        self.source_view_page.source_text_view.get_buffer().connect("changed", self.on_update_source)

        if not self.settings_manager.gsettings_available:
            self.show_banner(_("Settings schema could not be loaded. Selected settings will be lost on restart"))

    def show_start_page(self):
        self.navigation_view.replace([self.luminaire_content_page])

    def install_actions(self):

        self.add_action_entries(
            [
                ("open", self.on_open),
                ("new", self.on_new),
                ("show_ldc_zoom", self.on_show_ldc_zoom)
            ]
        )

        self.install_action("app.show_about_window", None, self.show_about_dialog)
        self.install_action("app.show_preferences", None, self.show_preferences)
        self.connect("close-request", self.on_close_request)

    def setup_accelerators(self):
        app = self.get_application()

    def display_photometry_content(self, luminaire: Luminaire):
        self.luminaire_content_page.set_photometry(luminaire)
        self.values_table_page.set_photometry(luminaire)
        self.ldc_export_page.set_photometry(luminaire)
        self.direct_ratios_page.set_photometry(luminaire)
        self.photometry_page.set_photometry(luminaire)
        self.geometry_page.set_photometry(luminaire)
        self.ldc_zoom_page.set_photometry(luminaire)
        self.photometry_export_page.set_photometry(luminaire)

        self.opened_photometry = luminaire

    def on_new(self, *args):
        stram = io.StringIO("")
        self.open_stream(stram)
        stram.seek(0)

    def on_open(self, *args):
        if self.source_view_page.source_text_view.get_buffer().get_modified():
            self.pending_action = "open"
            self.show_exit_dialog()
        else:
            self.open_file_chooser.show()

    def on_save(self, *args):
        if self.opened_file:
            buffer: Gtk.TextBuffer = self.source_view_page.source_text_view.get_buffer()
            start = buffer.get_start_iter()
            end = buffer.get_end_iter()
            write_string(self.opened_file, buffer.get_text(start, end, True))
            self.source_view_page.source_text_view.get_buffer().set_modified(False)
            self.resume_pending_action()
        else:
            self.on_save_as()

    def on_autosave(self, *args):
        if not self.opened_file:
            return

        if not self.settings_manager.settings.autosave:
            return

        self.on_save()

    def on_save_as(self, *args):
        self.save_as_file_chooser.show()

    def on_open_url(self, action, params: GLib.Variant, *args):
        Gtk.show_uri(self, params.get_string(), Gdk.CURRENT_TIME)

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            self.open_file(file)
        self.pending_action = None


    def on_save_as_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            buffer: Gtk.TextBuffer = self.source_view_page.source_text_view.get_buffer()
            start = buffer.get_start_iter()
            end = buffer.get_end_iter()
            write_string(dialog.get_file(), buffer.get_text(start, end, True))
            self.update_file(dialog.get_file())
            self.source_view_page.source_text_view.get_buffer().set_modified(False)
            self.resume_pending_action()
        else:
            self.pending_action = None

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

    def on_export_response(self, filename):
        self.show_start_page()
        self.show_banner(_("Exported as {}").format(filename))

    def on_title_visible_changed(self, *args):
        title_visible = self.window_title.get_title_visible()
        self.switcher_bar.set_reveal(title_visible)

    def on_drop(self, target, file, *args):
        self.open_file(file)
        return True

    def on_show_ldc_zoom(self, *args):
        self.navigation_view.push(self.ldc_zoom_page)

    def open_stream(self, f: IO):
        if self.is_opening:
            return

        try:
            self.is_opening = True
            photometry = import_from_file(f)

            self.display_photometry_content(photometry)

            self.add_action_entries(
                [
                    ("show_intensity_values", self.show_intensity_values),
                    ("show_source", self.show_source),
                    ("show_direct_ratios", self.show_direct_ratios),
                    ("show_photometry", self.show_photometry),
                    ("show_geometry", self.show_geometry),
                    ("show_lamp_set", self.show_lamp_set, "i"),
                    ("show_ballast", self.show_ballast, "i"),
                    ("export_luminaire_as_json", self.show_json_export_file_chooser),
                    ("export_intensities_as_csv", self.show_csv_export_file_chooser),
                    ("export_ldc_as_image", self.show_ldc_export_page),
                    ("export_photometry", self.show_photometry_export_page),
                    ("save", self.on_save),
                    ("autosave", self.on_autosave),
                    ("save_as", self.on_save_as),
                    ("open_url", self.on_open_url, "s")
                ]
            )
        finally:
            self.is_opening = False


    def update_file(self, file: Gio.File):
        self.opened_file = file
        filename = file.get_basename()
        self.set_title(title=filename)
        self.window_title.set_subtitle(filename)
        self.save_as_file_chooser.set_file(file)
        self.json_export_file_chooser.set_current_name(f"{filename}.json")
        self.csv_export_file_chooser.set_current_name(f"{filename}.csv")
        self.photometry_export_page.set_current_name(f"{filename}_exported")

    def open_file(self, file: Gio.File):
        try:
            with (gio_file_stream(file) as f):
                self.open_stream(f)
                f.seek(0)
                self.source_view_page.open_stream(f)
                self.update_file(file)
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
        window = PreferencesWindow()
        window.show()

    def show_source(self, *args):
        self.navigation_view.push(self.source_view_page)

    def show_direct_ratios(self, *args):
        self.navigation_view.push(self.direct_ratios_page)

    def show_photometry(self, *args):
        self.navigation_view.push(self.photometry_page)

    def show_geometry(self, *args):
        self.navigation_view.push(self.geometry_page)

    def show_lamp_set(self, action, params: GLib.Variant, *args):
        if self.opened_photometry is None:
            return

        lamp_index = params.get_int32()
        if len(self.opened_photometry.lamps) < lamp_index:
            return

        lamp_set = self.opened_photometry.lamps[lamp_index]

        self.lamp_set_page.set_lamp_set(self.opened_photometry, lamp_set)
        self.navigation_view.push(self.lamp_set_page)

    def show_ballast(self, action, params: GLib.Variant, *args):
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

    def show_photometry_export_page(self, *args):
        self.show_start_page()
        self.navigation_view.push(self.photometry_export_page)

    def show_ldc_export_page(self, *args):
        self.show_start_page()
        self.navigation_view.push(self.ldc_export_page)

    def on_update_source(self, buffer: Gtk.TextBuffer):
        self.is_dirty = True
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

    def on_close_request(self, *args):
        if self.pending_action == "close":
            return False

        is_file_changed = self.source_view_page.source_text_view.get_buffer().get_modified()
        if not is_file_changed:
           return False

        self.pending_action = "close"
        self.show_exit_dialog()
        return True

    def show_exit_dialog(self):
        dialog: Adw.MessageDialog = Adw.MessageDialog.new(
            parent=self,
            heading=_("Unsaved changes"),
            body=_("Do you want to save changes to the opened file before closing?"),
        )

        dialog.add_response("cancel", _("Cancel"))
        dialog.add_response("discard", _("Discard"))
        dialog.set_response_appearance("discard", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.add_response("save", _("Save"))
        dialog.set_response_appearance("save", Adw.ResponseAppearance.SUGGESTED)
        dialog.set_default_response("save")
        dialog.set_close_response("cancel")
        dialog.connect("response", self.on_exit_dialog_response)
        dialog.present()

    def on_exit_dialog_response(self, dialog: Adw.MessageDialog, response: str):
        match response:
            case "save":
                self.on_save()
            case "discard":
                self.resume_pending_action()
            case "cancel":
                dialog.close()
                self.pending_action = None

    def resume_pending_action(self):
        match self.pending_action:
            case "close":
                self.close()
            case "open":
                self.open_file_chooser.show()
        self.pending_action = None

    @staticmethod
    def show_about_dialog(*args):
        window = AboutWindow()
        window.show()
