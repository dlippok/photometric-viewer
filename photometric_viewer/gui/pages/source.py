import os

from gi.repository import Adw, Gtk, GtkSource
from gi.repository.Gtk import ScrolledWindow, PolicyType
from gi.repository.GtkSource import View

from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.model.luminaire import Luminaire, FileFormat
from photometric_viewer.utils.project import ASSETS_PATH

SPECS_DIR = os.path.join(ASSETS_PATH, "language-specs")

class SourceViewPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Source"), **kwargs)
        self.adw_style_manager: Adw.StyleManager = Adw.StyleManager.get_default()

        self.source_text_view = View(
            editable=True,
            monospace=True,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            pixels_below_lines=1,
            left_margin=20,
            right_margin=20,
            top_margin=20,
            bottom_margin=20,
        )

        self.source_text_view.set_show_line_numbers(True)

        self.lang_manager: GtkSource.LanguageManager = GtkSource.LanguageManager.get_default()
        self.lang_manager.append_search_path(SPECS_DIR)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.source_text_view)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)

        self.set_content(scrolled_window)

        self.adw_style_manager.connect("notify", self.update_theme)

        self.update_theme()

    def set_photometry(self, luminaire: Luminaire):
        self.source_text_view.get_buffer().set_text(luminaire.metadata.file_source)

        buffer: GtkSource.Buffer = self.source_text_view.get_buffer()

        if luminaire.metadata.file_format == FileFormat.IES:
            buffer.set_language(self.lang_manager.get_language("ies"))
        else:
            buffer.set_language(self.lang_manager.get_language("ldt"))

    def update_theme(self, *args):
        style_manager = GtkSource.StyleSchemeManager.get_default()
        buffer: GtkSource.Buffer = self.source_text_view.get_buffer()

        if self.adw_style_manager.get_dark():
            buffer.set_style_scheme(style_manager.get_scheme('Adwaita-dark'))
        else:
            buffer.set_style_scheme(style_manager.get_scheme('Adwaita'))