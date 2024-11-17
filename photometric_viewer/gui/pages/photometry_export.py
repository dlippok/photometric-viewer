import io
from datetime import datetime

from gi.repository import Adw, Gio, Gtk
from gi.repository.Gtk import Box, Orientation, Label, PolicyType, ScrolledWindow, FileFilter, FileChooserDialog, \
    Button, FileChooserNative
from gi.repository.Pango import WrapMode

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.formats import svg, png, ldt, ies
from photometric_viewer.gui.dialogs.file_chooser import ExportFileChooser
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.photomery_export.photometry_export_list import PhotometryExportList, \
    LdtExportProperties
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.gi.gio import write_bytes, write_string
from photometric_viewer.utils.project import PROJECT


class PhotometryExportPage(BasePage):
    def __init__(self, on_exported, transient_for: Gtk.Window, **kwargs):
        super().__init__(_("Export Photometric File"), **kwargs)
        self.current_name = _("untitled")
        self.luminaire = None
        self.on_exported = on_exported
        self.transient_for = transient_for

        box = Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16,
        )

        self.export_list = PhotometryExportList()
        box.append(self.export_list)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)

        export_box = Box(
            orientation=Orientation.VERTICAL
        )
        export_box.append(scrolled_window)

        export_button = Button(
                label=_("Export"),
                css_classes=["pill", "suggested-action"],
                halign=Gtk.Align.CENTER,
                margin_top=24,
                margin_bottom=24
            )
        export_button.connect("clicked", self.on_export_clicked)

        export_box.append(
            export_button
        )

        self.set_content(export_box)

    def set_current_name(self, current_name):
        self.current_name = current_name

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire

    def on_export_clicked(self, dialog: FileChooserDialog):
        self.show_file_chooser()

    def show_file_chooser(self):
        self.file_chooser = FileChooserNative(
            transient_for=self.transient_for,
            action=Gtk.FileChooserAction.SAVE,
            select_multiple=False,
            modal=True,
        )
        self.file_chooser.connect("response", self.on_export_response)

        if isinstance(self.export_list.get_current_properties(), LdtExportProperties):
            file_filter = FileFilter(name=_("EULUMDAT (*.ldt)"))
            file_filter.add_pattern("*.ldt")
            self.file_chooser.add_filter(file_filter)
            self.file_chooser.set_current_name(f"{self.current_name}.ldt")
        else:
            file_filter = FileFilter(name=_("IESNA (*.ies)"))
            file_filter.add_pattern("*.ies")
            self.file_chooser.add_filter(file_filter)
            self.file_chooser.set_current_name(f"{self.current_name}.ies")

        all_files_filter = FileFilter(name=_("All files"))
        all_files_filter.add_pattern("*")
        self.file_chooser.add_filter(all_files_filter)
        self.file_chooser.show()

    def on_export_response(self, dialog, response):
        if not self.luminaire:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        export_properties = self.export_list.get_current_properties()

        file: Gio.File = dialog.get_file()

        if isinstance(export_properties, LdtExportProperties):
            self.export_ldt(file, export_properties)
        else:
            self.export_ies(file, export_properties)

        self.on_exported(file.get_basename())

    def export_ldt(self, file: Gio.File, export_properties: LdtExportProperties):
        with io.StringIO() as f:
            ldt.export_to_file(f, self.luminaire)
            write_string(file, f.getvalue())

    def export_ies(self, file: Gio.File, export_properties: LdtExportProperties):
        export_keywords = {
            "_EXPORT_TOOL": PROJECT.name,
            "_EXPORT_TOOL_VERSION": PROJECT.version,
            "_EXPORT_TOOL_HOMEPAGE": PROJECT.urls.homepage,
            "_EXPORT_TOOL_ISSUE_TRACKER": PROJECT.urls.bug_tracker,
            "_EXPORT_TIMESTAMP": datetime.now().isoformat()
        }

        with io.StringIO() as f:
            ies.export_to_file(f, self.luminaire, export_keywords)
            write_string(file, f.getvalue())


