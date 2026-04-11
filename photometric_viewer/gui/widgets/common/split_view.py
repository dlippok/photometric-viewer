from gi.repository import Adw, Gtk
from gi.repository.Adw import NavigationView

from photometric_viewer.gui.pages.source import SourceViewPage


class SplitView(Adw.Bin):
    def __init__(self, source_view_page: SourceViewPage, navigation_view: NavigationView):
        super().__init__()
        self.overlay_split_view = Adw.OverlaySplitView()
        self.overlay_split_view.set_sidebar_width_fraction(0.4)
        self.overlay_split_view.set_max_sidebar_width(1000)
        self.overlay_split_view.set_pin_sidebar(True)
        self.overlay_split_view.set_content(source_view_page)
        self.overlay_split_view.set_sidebar(navigation_view)
        self.overlay_split_view.set_sidebar_position(Gtk.PackType.END)
        self.set_child(self.overlay_split_view)
        
