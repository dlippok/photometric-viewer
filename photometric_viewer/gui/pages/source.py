from gi.repository import Adw, Gtk, GtkSource
from gi.repository.Gtk import ScrolledWindow, PolicyType
from gi.repository.GtkSource import View

from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.model.luminaire import Luminaire


class SourceViewPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Source"), **kwargs)

        self.source_text_view = View(
            editable=False,
            monospace=True,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            pixels_below_lines=1,
        )

        self.source_text_view.set_show_line_numbers(True)
        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.source_text_view)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.source_text_view.get_buffer().set_text(luminaire.metadata.file_source)
