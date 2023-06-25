from gi.repository import Gtk
from gi.repository.Gtk import FileChooserNative, FileFilter


class FileChooser(FileChooserNative):
    def __init__(self, **kwargs):
        super().__init__(
            action=Gtk.FileChooserAction.OPEN,
            select_multiple=False,
            modal=True,
            **kwargs
        )

        photometric_filter = FileFilter(name=_("All photometric files"))
        photometric_filter.add_pattern("*.ies")
        photometric_filter.add_pattern("*.ldt")

        ies_filter = FileFilter(name=_("IESNA (*.ies)"))
        ies_filter.add_pattern("*.ies")

        ldt_filter = FileFilter(name=_("EULUMDAT (*.ldt)"))
        ldt_filter.add_pattern("*.ldt")

        all_files_filter = FileFilter(name=_("All Files"))
        all_files_filter.add_pattern("*")

        self.add_filter(photometric_filter)
        self.add_filter(ies_filter)
        self.add_filter(ldt_filter)
        self.add_filter(all_files_filter)
