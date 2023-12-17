from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType

from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.model.luminaire import Luminaire


class SourceViewPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Source"), **kwargs)

        self.source_text_view = Gtk.TextView(
            editable=False,
            monospace=True,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            left_margin=20,
            right_margin=20,
            top_margin=20,
            bottom_margin=20,
            pixels_below_lines=1,

        )

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.source_text_view)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.source_text_view.get_buffer().set_text(luminaire.metadata.file_source)
