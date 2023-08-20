from gi.repository import Gtk
from gi.repository.Gtk import FileChooserNative, FileFilter


class ExportFileChooser(FileChooserNative):
    def __init__(self, **kwargs):
        super().__init__(
            action=Gtk.FileChooserAction.SAVE,
            select_multiple=False,
            modal=True,
            **kwargs
        )

    def _add_all_files_filter(self):
        all_files_filter = FileFilter(name=_("All files"))
        all_files_filter.add_pattern("*")
        self.add_filter(all_files_filter)

    @staticmethod
    def for_json(**kwargs):
        chooser = ExportFileChooser(**kwargs)

        json_filter = FileFilter(name=_("JSON files"))
        json_filter.add_pattern("*.json")
        chooser.add_filter(json_filter)
        chooser._add_all_files_filter()

        return chooser

    @staticmethod
    def for_csv(**kwargs):
        chooser = ExportFileChooser(**kwargs)

        csv_filter = FileFilter(name=_("CSV files"))
        csv_filter.add_pattern("*.csv")
        chooser.add_filter(csv_filter)
        chooser._add_all_files_filter()

        return chooser

    @staticmethod
    def for_ldc(**kwargs):
        chooser = ExportFileChooser(**kwargs)

        png_filter = FileFilter(name=_("PNG raster graphics"))
        png_filter.add_pattern("*.png")
        chooser.add_filter(png_filter)
        svg_filter = FileFilter(name=_("SVG vector graphics"))
        svg_filter.add_pattern("*.svg")
        chooser.add_filter(svg_filter)
        chooser._add_all_files_filter()

        return chooser

    @staticmethod
    def for_ldt(**kwargs):
        chooser = ExportFileChooser(**kwargs)

        file_filter = FileFilter(name=_("EULUMDAT (*.ldt)"))
        file_filter.add_pattern("*.ldt")
        chooser.add_filter(file_filter)
        chooser._add_all_files_filter()

        return chooser

    @staticmethod
    def for_ies(**kwargs):
        chooser = ExportFileChooser(**kwargs)

        file_filter = FileFilter(name=_("IESNA (*.ies)"))
        file_filter.add_pattern("*.ies")
        chooser.add_filter(file_filter)
        chooser._add_all_files_filter()

        return chooser


class OpenFileChooser(FileChooserNative):
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
