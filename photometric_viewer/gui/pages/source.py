import os
import typing

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
        self.source_text_view.get_buffer().connect("changed", self.on_update_content)

        self.lang_manager: GtkSource.LanguageManager = GtkSource.LanguageManager.get_default()
        self.lang_manager.append_search_path(SPECS_DIR)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.source_text_view)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)

        self.set_content(scrolled_window)

        self.adw_style_manager.connect("notify", self.update_theme)

        self.update_theme()

    def on_update_content(self, *args):
        self._update_language()

    def open_stream(self, f: typing.IO):
        self.source_text_view.get_buffer().set_text(f.read())
        self.source_text_view.get_buffer().set_modified(False)

    def _update_language(self):
        buffer: Gtk.TextBuffer = self.source_text_view.get_buffer()
        start = buffer.get_start_iter()
        end: Gtk.TextIter = buffer.get_start_iter()
        end.forward_line()
        text = buffer.get_text(start, end, True)

        if text.lower().startswith("iesna"):
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