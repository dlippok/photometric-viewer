from gi.repository import Adw, Gtk
from gi.repository.Adw import NavigationView

from photometric_viewer.gui.pages.source import SourceViewPage


class SplitView(Adw.Bin):
    def __init__(self, source_view_page: SourceViewPage, navigation_view: NavigationView):
        super().__init__()
        overlay_split_view = Adw.OverlaySplitView()
        overlay_split_view.set_sidebar_width_fraction(0.3)
        overlay_split_view.set_max_sidebar_width(8000)
        overlay_split_view.set_min_sidebar_width(400)
        overlay_split_view.set_content(source_view_page)
        overlay_split_view.set_sidebar(navigation_view)
        overlay_split_view.set_sidebar_position(Gtk.PackType.END)
        self.set_child(overlay_split_view)