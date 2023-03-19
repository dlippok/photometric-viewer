from gi.repository import Adw, Gtk, Gio
from gi.repository.Gtk import Label, Separator, PackType, Orientation, ScrolledWindow, PolicyType, Button, \
    FileChooserDialog, Filter, FileFilter

from photometric_viewer.formats.ies import import_from_file
from photometric_viewer.gui.content import MainContent
from photometric_viewer.model.photometry import Photometry


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_default_size(500, 600)
        self.set_title(title='IES preview')

        self.main_content = MainContent()

        clamp = Adw.Clamp()
        clamp.set_child(self.main_content)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
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
        dialog.show()

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            with open(file.get_path()) as f:
                self.open_photometry(import_from_file(f))
        dialog.close()

    def open_photometry(self, photometry: Photometry):
        if photometry.metadata.luminaire:
            self.set_title(title=photometry.metadata.luminaire)
        self.main_content.set_photometry(photometry)

