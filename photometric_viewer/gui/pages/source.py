from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType

from photometric_viewer.model.luminaire import Luminaire


class SourceViewPage(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.source_text_view = Gtk.TextView(
            editable=False,
            monospace=True,
            wrap_mode=Gtk.WrapMode.WORD_CHAR,
            left_margin=7,
            right_margin=7,
            top_margin=7,
            bottom_margin=7
        )

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(self.source_text_view)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_child(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.source_text_view.get_buffer().set_text(luminaire.metadata.file_source)
