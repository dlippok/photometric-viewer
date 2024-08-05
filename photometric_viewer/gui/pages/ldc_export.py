from gi.repository import Adw, Gio, Gtk
from gi.repository.Gtk import Box, Orientation, Label, PolicyType, ScrolledWindow, FileFilter, FileChooserDialog
from gi.repository.Pango import WrapMode

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.formats import svg, png
from photometric_viewer.gui.dialogs.file_chooser import ExportFileChooser
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.ldc_export.diagram import PhotometricDiagramPreview
from photometric_viewer.gui.widgets.ldc_export.file_properties import LdcExportFilePropertiesBox, \
    LdcExportFileProperties, LdcExportFileType
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.gi.gio import write_bytes


class LdcExportPage(BasePage):
    def __init__(self, on_exported, transient_for: Gtk.Window, **kwargs):
        super().__init__(_("Export Light Distribution Curve"), **kwargs)

        self.file_chooser = ExportFileChooser(transient_for=transient_for)
        self.transient_for = transient_for

        self.luminaire = None
        self.on_exported = on_exported

        box = Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16,
        )

        self.properties_box = LdcExportFilePropertiesBox(
            on_properties_changed=self.properties_changed,
            on_export_clicked=self.on_export_clicked
        )
        box.append(self.properties_box)

        preview_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            label=_("Preview")
        )
        box.append(preview_label)

        self.diagram = PhotometricDiagramPreview()
        box.append(self.diagram)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.diagram.set_photometry(luminaire)
        self.properties_box.update()

    def properties_changed(self, properties: LdcExportFileProperties):
        self.diagram.update_settings(properties.plotter_settings)

    def on_export_clicked(self):
        self.file_chooser = ExportFileChooser(transient_for=self.transient_for)

        match self.properties_box.properties.file_type:
            case LdcExportFileType.PNG:
                self.file_chooser.set_current_name("photometry.png")
                png_filter = FileFilter(name=_("PNG raster graphics"))
                png_filter.add_pattern("*.png")
                self.file_chooser.add_filter(png_filter)
                self.file_chooser.connect("response", self.on_export_png_response)
            case LdcExportFileType.SVG:
                self.file_chooser.set_current_name("photometry.svg")
                svg_filter = FileFilter(name=_("SVG vector graphics"))
                svg_filter.add_pattern("*.svg")
                self.file_chooser.add_filter(svg_filter)
                self.file_chooser.connect("response", self.on_export_svg_response)

        self.file_chooser._add_all_files_filter()
        self.file_chooser.show()

    def on_export_png_response(self, dialog: FileChooserDialog, response):
        if not self.luminaire:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()
        data = png.export_photometry(
            self.luminaire,
            self.properties_box.properties.size_in_px,
            self.properties_box.properties.plotter_settings
        )
        write_bytes(file, data)
        self.on_exported(file.get_basename())

    def on_export_svg_response(self, dialog: FileChooserDialog, response):
        if not self.luminaire:
            return

        if response != Gtk.ResponseType.ACCEPT:
            return

        file: Gio.File = dialog.get_file()
        data = svg.export_photometry(
            self.luminaire,
            self.properties_box.properties.size_in_px,
            self.properties_box.properties.plotter_settings
        )
        write_bytes(file, data)
        self.on_exported(file.get_basename())
