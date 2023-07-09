import math

import cairo
from photometric_viewer.model.photometry import Photometry
from photometric_viewer.utils.coordinates import cartesian_to_screen


def _get_max_candela(photometry: Photometry):
    max_candelas = 0

    for c_angle in [0, 90, 180, 270]:
        values = photometry.get_values_for_c_angle(c_angle)
        for angle, candelas in values.items():
            if candelas > max_candelas:
                max_candelas = candelas

    return max_candelas


class LightDistributionPlotter:
    def __init__(self):
        self.size = 300

    def draw(self, context: cairo.Context, photometry: Photometry):
        self._draw_coordinate_system(context, photometry)
        self._draw_curve(context, photometry)
        self._draw_legend(context)

    def _draw_coordinate_system(self, context: cairo.Context, photometry: Photometry):
        center = self.size / 2, self.size / 2

        context.set_line_width(1)
        context.set_dash([4])
        context.set_source_rgb(0.6, 0.6, 0.6)

        radii = [
            int((self.size - 50) * 1 / 6),
            int((self.size - 50) * 2 / 6),
            int((self.size - 50) * 3 / 6),
        ]

        # Draw circles
        for radius in radii:
            context.arc(center[0], center[1], radius, 0, 2 * math.pi)
            context.stroke()

        # Draw spokes
        for angle in [math.pi * x / 4 for x in range(8)]:
            context.move_to(self.size / 2, self.size / 2)
            point = cartesian_to_screen(center, (math.cos(angle) * self.size, math.sin(angle) * self.size))
            point_clipped_to_canvas = (
                min(self.size, max(0, point[0])),
                min(self.size, max(1, point[1]))
            )
            context.line_to(point_clipped_to_canvas[0], point_clipped_to_canvas[1])
            context.stroke()

        self.draw_values(center, context, photometry, radii)

    @staticmethod
    def draw_values(center, context, photometry, radii):
        max_candelas = _get_max_candela(photometry)
        for n, radius in enumerate(radii):
            unit = "cd" if photometry.is_absolute else "cd/klm"
            value = max_candelas * (n + 1) / 3

            text = f"{value:.0f} {unit}"
            extents = context.text_extents(text)
            first_value_point = cartesian_to_screen(center, (-(extents.width / 2), -radius - 15))
            context.move_to(first_value_point[0], first_value_point[1])
            context.show_text(text)

    def _draw_curve(self, context: cairo.Context, photometry: Photometry):
        context.set_line_width(2)
        context.set_source_rgba(0.8, 0.8, 0, 0.4)

        max_candelas = _get_max_candela(photometry)

        context.set_dash([])
        self._draw_halfcurve(context, photometry, max_candelas, 0)
        self._draw_halfcurve(context, photometry, max_candelas, 180)

        context.set_dash([2])
        self._draw_halfcurve(context, photometry, max_candelas, 90)
        self._draw_halfcurve(context, photometry, max_candelas, 270)

    def _draw_halfcurve(self, context: cairo.Context, photometry: Photometry, max_candelas, c_angle):
        center = self.size / 2, self.size / 2
        max_candelas_scale = int((self.size - 50) * 3 / 6)
        angle_modifier = 1 if c_angle < 180 else -1

        context.new_path()
        is_first_point = True
        for angle, candelas in photometry.get_values_for_c_angle(c_angle).items():
            distance = candelas / max_candelas * max_candelas_scale
            angle = math.radians(angle)
            cartesian_point = (
                math.cos(angle_modifier * angle - math.pi / 2) * distance,
                math.sin(angle_modifier * angle - math.pi / 2) * distance
            )
            point = cartesian_to_screen(center, cartesian_point)
            if is_first_point:
                context.move_to(point[0], point[1])
                is_first_point = False
            else:
                context.line_to(int(point[0]), int(point[1]))

        context.set_source_rgba(0.8, 0.8, 0, 0.4)
        context.stroke_preserve()

        context.set_source_rgba(0.8, 0.8, 0, 0.2)
        context.fill()

    def _draw_legend(self, context: cairo.Context):
        context.set_line_width(2)

        context.new_path()
        context.set_dash([])

        context.set_source_rgba(0.8, 0.8, 0, 0.6)
        context.move_to(self.size - 100, self.size - 20)
        context.line_to(self.size - 100 + 15, self.size - 20)
        context.stroke()

        context.new_path()
        context.move_to(self.size - 100 + 18, self.size - 17)
        context.set_source_rgb(0.6, 0.6, 0.6)
        context.show_text("C0-C180")
        context.stroke()

        context.new_path()
        context.set_dash([2])

        context.set_source_rgba(0.8, 0.8, 0, 0.6)
        context.move_to(self.size - 100, self.size - 8)
        context.line_to(self.size - 100 + 15, self.size - 8)
        context.stroke()

        context.new_path()
        context.move_to(self.size - 100 + 18, self.size - 5)
        context.set_source_rgb(0.6, 0.6, 0.6)
        context.show_text("C90-C270")
        context.stroke()
