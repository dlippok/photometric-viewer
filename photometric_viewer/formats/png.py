import io

import cairo

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.plotters import LightDistributionPlotter, LightDistributionPlotterSettings


def export_photometry(luminaire: Luminaire, size: int, settings: LightDistributionPlotterSettings):
    plotter = LightDistributionPlotter(settings=settings)
    surface = cairo.ImageSurface(cairo.Format.ARGB32, size,  size)
    plotter.size = size
    context = cairo.Context(surface)
    plotter.draw(context, luminaire)
    bytes_io = io.BytesIO()
    surface.write_to_png(bytes_io)
    return bytes_io.getvalue()

