import io

import cairo

from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils import plotter_themes
from photometric_viewer.utils.plotters import LightDistributionPlotter, LightDistributionPlotterSettings


def export_photometry(photometry: Photometry):
    plotter = LightDistributionPlotter(settings=LightDistributionPlotterSettings(theme=plotter_themes.THEMES[0].plotter_theme))
    surface = cairo.ImageSurface(cairo.Format.RGB24, 1000,  1000)
    plotter.size = 1000
    context = cairo.Context(surface)
    context.rectangle(0, 0, 1000, 1000)
    context.set_source_rgb(1, 1, 1)
    context.fill()
    plotter.draw(context, photometry)
    bytes_io = io.BytesIO()
    surface.write_to_png(bytes_io)
    return bytes_io.getvalue()

