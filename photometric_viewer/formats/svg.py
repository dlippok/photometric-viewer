import io

import cairo

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.plotters import LightDistributionPlotter, LightDistributionPlotterSettings


def export_photometry(luminaire: Luminaire, size: int, settings: LightDistributionPlotterSettings):
    plotter = LightDistributionPlotter(settings=settings)
    bytes_io = io.BytesIO()
    surface = cairo.SVGSurface(bytes_io, size,  size)
    plotter.size = size
    context = cairo.Context(surface)
    plotter.draw(context, luminaire)
    surface.finish()
    return bytes_io.getvalue()

