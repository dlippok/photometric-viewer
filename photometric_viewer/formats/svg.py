import io

import cairo

from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.plotters import LightDistributionPlotter


def export_photometry(photometry: Photometry):
    plotter = LightDistributionPlotter()
    bytes_io = io.BytesIO()
    surface = cairo.SVGSurface(bytes_io, 1000,  1000)
    plotter.size = 1000
    context = cairo.Context(surface)
    context.rectangle(0, 0, 1000, 1000)
    context.set_source_rgb(1, 1, 1)
    context.fill()
    plotter.draw(context, photometry)
    surface.finish()
    return bytes_io.getvalue()

