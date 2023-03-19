import math

import cairo
from gi.repository import Gtk

from model.photometry import Photometry
from utils.plotters import LightDistributionPlotter


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





