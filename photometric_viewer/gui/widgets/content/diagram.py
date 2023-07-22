import cairo
from gi.repository import Gtk

from photometric_viewer.model.photometry import Photometry
from photometric_viewer.model.settings import Settings
from photometric_viewer.utils.plotters import LightDistributionPlotter, DiagramStyle, SnapValueAnglesTo, \
    DisplayHalfSpaces


class PhotometricDiagram(Gtk.DrawingArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list"])
        self.set_draw_func(self.on_draw)
        self.photometry = None
        self.plotter = LightDistributionPlotter()

    def on_draw(self, _, context: cairo.Context, width, height):
        self.set_content_height(width)
        self.set_name("photometric_diagram")
        self.plotter.size = width
        self.plotter.draw(context, self.photometry)

    def set_photometry(self, photometry: Photometry):
        self.photometry = photometry
        self.queue_draw()

    def update_settings(self, settings: Settings):
        self.plotter.settings.style = DiagramStyle(settings.diagram_style.value)
        self.plotter.settings.snap_value_angles_to = SnapValueAnglesTo(settings.snap_value_angles_to.value)
        self.plotter.settings.display_half_spaces = DisplayHalfSpaces(settings.display_half_spaces.value)
        self.queue_draw()
