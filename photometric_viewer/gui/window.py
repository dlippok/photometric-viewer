from typing import Optional

from gi.repository import Adw, Gtk, Gio
from gi.repository.Adw import ViewStackPage
from gi.repository.Gtk import Label, Orientation, ScrolledWindow, PolicyType, Button, \
    FileChooserDialog, FileFilter, FileChooserNative

from photometric_viewer.formats.common import import_from_file
from photometric_viewer.gui.about import AboutWindow
from photometric_viewer.gui.content import PhotometryContent

from photometric_viewer.gui.empty import EmptyPage
from photometric_viewer.gui.menu import ApplicationMenuButton
from photometric_viewer.gui.source import SourceView
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.io import gio_file_stream


class MainWindow(Adw.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opened_photometry: Optional[Photometry] = None

        self.set_default_size(550, 700)
        self.set_title(title='Photometric Viewer')

        self.install_action("app.show_about_window", None, self.show_about_dialog)

        self.content_bin = Adw.Bin()
        self.content_bin.set_child(EmptyPage())
        self.content_bin.set_vexpand(True)

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
        box.append(self.content_bin)

        photometric_filter = FileFilter(name="All photometric files")
        photometric_filter.add_pattern("*.ies")
        photometric_filter.add_pattern("*.ldt")

        ies_filter = FileFilter(name="IESNA (*.ies)")
        ies_filter.add_pattern("*.ies")

        ldt_filter = FileFilter(name="Eulumdat (*.ldt)")
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
        photometry_content = PhotometryContent()
        photometry_content.set_photometry(photometry)

        source_view = SourceView()
        source_view.set_photometry(photometry)

        view_stack = Adw.ViewStack()

        properties_page: ViewStackPage = view_stack.add_titled(photometry_content, "photometry", "Photometry")
        properties_page.set_icon_name("view-reveal-symbolic")

        source_page: ViewStackPage = view_stack.add_titled(source_view, "source", "Source")
        source_page.set_icon_name("view-paged-symbolic")

        self.content_bin.set_child(view_stack)
        self.switcher_bar.set_stack(view_stack)
        self.opened_photometry = photometry

    def on_open_clicked(self, button):
        self.file_chooser.show()

    def on_open_response(self, dialog: FileChooserDialog, response):
        if response == Gtk.ResponseType.ACCEPT:
            file: Gio.File = dialog.get_file()
            with gio_file_stream(file) as f:
                self.open_photometry(import_from_file(f))

    def open_photometry(self, photometry: Photometry):
        if photometry.metadata.luminaire:
            self.set_title(title=photometry.metadata.luminaire)
        self.display_photometry_content(photometry)

    def show_about_dialog(self, *args):
        window = AboutWindow()
        window.show()
