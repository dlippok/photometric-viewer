import os
import time
import typing
from concurrent.futures import ThreadPoolExecutor

from gi.repository import Adw, Gtk, GtkSource
from gi.repository.Gtk import ScrolledWindow, PolicyType, WrapMode
from gi.repository.GtkSource import View

from photometric_viewer.gui.widgets.headerbar import default_headerbar
from photometric_viewer.model.settings import Settings
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.utils.project import ASSETS_PATH
from photometric_viewer.utils.gi.GSettings import SettingsManager

SPECS_DIR = os.path.join(ASSETS_PATH, "language-specs")

class SourceViewPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Source"), headerbar=default_headerbar(), show_title=False, **kwargs)
        self.adw_style_manager: Adw.StyleManager = Adw.StyleManager.get_default()
        self.settings_manager = SettingsManager()

        self.source_text_view = View(
            editable=True,
            monospace=True,
            pixels_below_lines=1,
            left_margin=20,
            right_margin=20,
            top_margin=20,
            bottom_margin=20,
        )

        self.executor = ThreadPoolExecutor(max_workers=1)

        self.lang_manager: GtkSource.LanguageManager = GtkSource.LanguageManager.get_default()
        self.lang_manager.append_search_path(SPECS_DIR)

        self.scrolled_window = ScrolledWindow()
        self.scrolled_window.set_child(self.source_text_view)
        self.scrolled_window.set_vexpand(True)

        self.set_content(self.scrolled_window)

        self.update_theme()

        self._on_update_settings(self.settings_manager.settings)
        self.settings_manager.register_on_update(self._on_update_settings)
        self._connect_signals()

    def on_update_content(self, *args):
        self.executor.submit(self._update_language)

    def on_shown(self, *args):
        self.source_text_view.grab_focus()

    def on_source_text_view_focus_change(self, *args):
        if not self.source_text_view.has_focus():
            self.activate_action("win.autosave")

    def open_stream(self, f: typing.IO):
        try:
            self.opening = True
            self.source_text_view.get_buffer().set_text(f.read())
            self.source_text_view.get_buffer().set_modified(False)
        finally:
            self.opening = False

    def _update_language(self):
        time.sleep(0.1)
        while self.opening:
            time.sleep(0.05)

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

    def _connect_signals(self):
        self.connect("shown", self.on_shown)
        self.source_text_view.get_buffer().connect("changed", self.on_update_content)
        self.adw_style_manager.connect("notify", self.update_theme)
        self.source_text_view.connect("notify::has-focus", self.on_source_text_view_focus_change)

    def _on_update_settings(self, settings: Settings):
        if settings.editor_word_warp:
            self.source_text_view.set_wrap_mode(WrapMode.WORD_CHAR)
            self.scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        else:
            self.source_text_view.set_wrap_mode(WrapMode.NONE)
            self.scrolled_window.set_policy(PolicyType.AUTOMATIC, PolicyType.AUTOMATIC)

        if settings.editor_grid:
            self.source_text_view.set_background_pattern(GtkSource.BackgroundPatternType.GRID)
        else:
            self.source_text_view.set_background_pattern(GtkSource.BackgroundPatternType.NONE)

        self.source_text_view.set_highlight_current_line(settings.editor_highlight_current_line)
        self.source_text_view.set_show_line_numbers(settings.editor_show_line_numbers)