from gi.repository import Adw, Gtk, Gio
from gi.repository.Gtk import Label, Orientation, ScrolledWindow, PolicyType, Button, \
    FileChooserDialog, FileFilter

from photometric_viewer.formats.ies import import_from_file
from photometric_viewer.gui.content import PhotometryContent
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.io import gio_file_stream


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opened_photometry = None

        self.set_default_size(600, 600)
        self.set_title(title='Photometric Viewer')

        self.clamp = Adw.Clamp()

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)

        open_button = Button(label="Open")
        open_button.connect("clicked", self.on_open_clicked)

        box = Gtk.Box(orientation=Orientation.VERTICAL)
        header_bar = Adw.HeaderBar()
        header_bar.pack_start(open_button)
        box.append(header_bar)
        box.append(scrolled_window)

        self.set_content(box)
        self.display_empty_content()

    def display_photometry_content(self, photometry):
        photometry_content = PhotometryContent()
        photometry_content.set_photometry(photometry)
        self.clamp.set_child(photometry_content)
        self.opened_photometry = photometry

    def display_empty_content(self):
        box = Gtk.Box(orientation=Orientation.VERTICAL, valign=Gtk.Align.CENTER, spacing=16)

        box.append(Label(label="No content", name="no-content-header"))
        box.append(Label(label="Open photometric file to display it here", name="no-content-subtitle"))
        self.clamp.set_child(box)

    def on_open_clicked(self, button):
        ies_filter = FileFilter(name="IESNA (*.ies)")
        ies_filter.add_pattern("*.ies")

        all_files_filter = FileFilter(name="All Files")
        all_files_filter.add_pattern("*")

        dialog = FileChooserDialog()
        dialog.connect("response", self.on_open_response)
        dialog.add_button("Open", Gtk.ResponseType.ACCEPT)
        dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_filter(ies_filter)
        dialog.add_filter(all_files_filter)
        dialog.set_transient_for(self)
        dialog.show()

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            with gio_file_stream(file) as f:
                self.open_photometry(import_from_file(f))
        dialog.close()

    def open_photometry(self, photometry: Photometry):
        if photometry.metadata.luminaire:
            self.set_title(title=photometry.metadata.luminaire)
        self.display_photometry_content(photometry)
