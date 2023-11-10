import cairo
from gi.repository import Gtk

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.plotters import LightDistributionPlotter, LightDistributionPlotterSettings


class PhotometricDiagramPreview(Gtk.DrawingArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_css_classes(["boxed-list"])
        self.set_name("photometric_diagram")
        self.set_draw_func(self.on_draw)
        self.luminaire = None
        self.plotter = LightDistributionPlotter()

    def draw_checkered_background(self, context: cairo.Context, width, height):
        context.save()
        context.set_source_rgba(0.5, 0.5, 0.5, 0.2)
        for y in range(0, height, 10):
            for x in range(0, width, 20):
                x_offset = 0 if y % 20 == 0 else 10
                context.rectangle(x + x_offset, y, 10, 10)
                context.fill()

        context.restore()

    def on_draw(self, _, context: cairo.Context, width, height):
        if self.luminaire is None:
            return

        self.set_content_height(width)
        self.plotter.size = width
        self.draw_checkered_background(context, width, height)
        self.plotter.draw(context, self.luminaire)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        self.queue_draw()

    def update_settings(self, settings: LightDistributionPlotterSettings):
        self.plotter.settings = settings
        self.queue_draw()