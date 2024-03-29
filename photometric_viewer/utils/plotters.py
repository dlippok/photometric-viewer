import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, List

import cairo

from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils.coordinates import cartesian_to_screen


class DiagramStyle(Enum):
    SIMPLE = 1
    DETAILED = 2


class SnapValueAnglesTo(Enum):
    MAX_VALUE = 1
    ROUND_NUMBER = 2


class DisplayHalfSpaces(Enum):
    BOTH = 1
    ONLY_RELEVANT = 2


@dataclass
class LightDistributionPlotterTheme:
    background_color: Tuple[float, float, float, float] | None = None
    coordinate_line_width: float = 1
    coordinate_line_dash: List[float] = (4,)
    coordinate_color: Tuple[float, float, float, float] = (0.6, 0.6, 0.6, 1)
    text_color: Tuple[float, float, float, float] = (0.6, 0.6, 0.6, 1)
    curve_line_width: float = 2
    c0_stroke: Tuple[float, float, float, float] = (0.8, 0.8, 0, 0.4)
    c0_fill: Tuple[float, float, float, float] | None = (0.8, 0.8, 0, 0.2)
    c0_dash: List[float] = ()
    c180_stroke: Tuple[float, float, float, float] = (0.8, 0.8, 0.0, 0.4)
    c180_fill: Tuple[float, float, float, float] | None = (0.8, 0.8, 0, 0.2)
    c180_dash: List[float] = (2,)


@dataclass
class LightDistributionPlotterSettings:
    style: DiagramStyle = DiagramStyle.DETAILED
    show_legend: bool = True
    show_values: bool = True
    snap_value_angles_to: SnapValueAnglesTo | int = SnapValueAnglesTo.ROUND_NUMBER
    display_half_spaces: DisplayHalfSpaces = DisplayHalfSpaces.ONLY_RELEVANT
    theme: LightDistributionPlotterTheme = field(default_factory=lambda : LightDistributionPlotterTheme())


class LightDistributionPlotter:
    def __init__(self, settings: LightDistributionPlotterSettings = None):
        self.size = 300
        self.center = (150, 150)
        if settings is not None:
            self.settings = settings
        else:
            self.settings = LightDistributionPlotterSettings()

    def _get_max_value_ratio(self):
        if self.center[1] == self.size / 2:
            return 0.4
        else:
            return 0.72

    def draw(self, context: cairo.Context, luminaire: Luminaire):
        self.center = self._get_center(luminaire)
        self._draw_background(context)

        try:
            self._draw_curve(context, luminaire)
        except ZeroDivisionError:
            pass

        self._draw_coordinate_system(context, luminaire)
        self._draw_legend(context)

    def _get_center(self, luminaire: Luminaire):
        if self.settings.display_half_spaces == DisplayHalfSpaces.BOTH:
            return self.size / 2, self.size / 2

        max_lower_half = 0
        max_upper_half = 0
        max_other = 0
        for c_angle in [0, 90, 180, 270]:
            values = luminaire.get_values_for_c_angle(c_angle)
            for angle, candelas in values.items():
                if angle < 45 and candelas > max_lower_half:
                    max_lower_half = candelas
                if angle >= 135 and candelas > max_upper_half:
                    max_upper_half = candelas
                if 45 <= angle < 135 and candelas > max_other:
                    max_other = candelas

        if max_other > max_upper_half and max_other > max_lower_half:
            return self.size / 2, self.size / 2
        elif max_upper_half < 0.1 * max_lower_half:
            return self.size / 2, self.size * 0.1
        elif max_lower_half < 0.1 * max_upper_half:
            return self.size / 2, self.size * 0.9
        else:
            return self.size / 2, self.size * 0.5

    def _get_max_candela(self, luminaire: Luminaire):
        max_candelas = 0

        for c_angle in [0, 90, 180, 270]:
            values = luminaire.get_values_for_c_angle(c_angle)
            for angle, candelas in values.items():
                if candelas > max_candelas:
                    max_candelas = candelas

        if self.settings.snap_value_angles_to == SnapValueAnglesTo.MAX_VALUE:
            return max_candelas

        if type(self.settings.snap_value_angles_to) == int:
            return self.settings.snap_value_angles_to

        round_values = [30, 48, 60, 90, 100,
                        300, 480, 600, 900, 1000,
                        3000, 4800, 6000, 9000, 10000,
                        30000, 48000, 60000, 90000, 100000]

        last_round_value = 0
        for round_value in round_values:
            if max_candelas > last_round_value:
                last_round_value = round_value

        return last_round_value

    def _draw_background(self, context: cairo.Context):
        if self.settings.theme.background_color is None:
            return
        context.set_source_rgba(
            self.settings.theme.background_color[0],
            self.settings.theme.background_color[1],
            self.settings.theme.background_color[2],
            self.settings.theme.background_color[3]
        )
        context.rectangle(0, 0, self.size, self.size)
        context.fill()

    def _draw_coordinate_system(self, context: cairo.Context, luminaire: Luminaire):
        context.set_line_width(self.settings.theme.coordinate_line_width)
        context.set_dash(self.settings.theme.coordinate_line_dash)
        r, g, b, a = self.settings.theme.coordinate_color
        context.set_source_rgba(r, g, b, a)

        ratio = self._get_max_value_ratio()

        if self.settings.style == DiagramStyle.SIMPLE:
            radii = [
                int(self.size * 0.3333 * ratio),
                int(self.size * 0.6666 * ratio),
                int(self.size * 1 * ratio),
                int(self.size * 1.3333 * ratio),
                int(self.size * 1.6666 * ratio),
            ]
        else:
            radii = [
                int(self.size * 0.25 * ratio),
                int(self.size * 0.5 * ratio),
                int(self.size * 0.75 * ratio),
                int(self.size * 1 * ratio),
                int(self.size * 1.25 * ratio),
                int(self.size * 1.5 * ratio),
            ]

        # Draw circles
        for radius in radii:
            context.arc(self.center[0], self.center[1], radius, 0, 2 * math.pi)
            context.stroke()

        # Draw spokes
        n_spokes = 8 if self.settings.style == DiagramStyle.SIMPLE else 16
        for angle in [math.pi * x / (n_spokes / 2) for x in range(n_spokes)]:
            context.move_to(self.center[0], self.center[1])
            point = cartesian_to_screen(self.center, (math.cos(angle) * self.size, math.sin(angle) * self.size))
            point_clipped_to_canvas = (
                point[0], point[1]
            )
            context.line_to(point_clipped_to_canvas[0], point_clipped_to_canvas[1])
            context.stroke()

        self.draw_values(self.center, context, luminaire, radii)

    def draw_values(self, center, context, luminaire, radii: List[int]):
        if not self.settings.show_values:
            return

        r, g, b, a = self.settings.theme.text_color
        context.set_source_rgba(r, g, b, a)

        max_candelas = self._get_max_candela(luminaire)
        for n, radius in enumerate(radii):
            unit = "cd" if luminaire.photometry.is_absolute else "cd/klm"
            value = max_candelas * (n + 1) / (len(radii) - 2)

            text = f"{value:.0f} {unit}"
            extents = context.text_extents(text)
            if center[1] > 0.5 * self.size:
                first_value_point = cartesian_to_screen(center, (-(extents.width / 2), float(radius - 15)))
            else:
                first_value_point = cartesian_to_screen(center, (-(extents.width / 2), float(-radius - 15)))

            context.move_to(first_value_point[0], first_value_point[1])
            context.show_text(text)

    def _draw_curve(self, context: cairo.Context, luminaire: Luminaire):
        theme = self.settings.theme
        context.set_line_width(theme.curve_line_width)
        max_candelas = self._get_max_candela(luminaire)

        context.set_dash(self.settings.theme.c0_dash)
        self._draw_halfcurve(context, luminaire, max_candelas, 0, theme.c0_stroke, theme.c0_fill)
        self._draw_halfcurve(context, luminaire, max_candelas, 180, theme.c0_stroke, theme.c0_fill)

        context.set_dash(self.settings.theme.c180_dash)
        self._draw_halfcurve(context, luminaire, max_candelas, 90, theme.c180_stroke, theme.c180_fill)
        self._draw_halfcurve(context, luminaire, max_candelas, 270, theme.c180_stroke, theme.c180_fill)

    def _draw_halfcurve(
            self,
            context: cairo.Context,
            luminaire: Luminaire,
            max_candelas,
            c_angle,
            stroke,
            fill
    ):
        max_candelas_scale = int(self.size * self._get_max_value_ratio())
        angle_modifier = 1 if c_angle < 180 else -1

        context.new_path()
        is_first_point = True
        for angle, candelas in luminaire.get_values_for_c_angle(c_angle).items():
            distance = candelas / max_candelas * max_candelas_scale
            angle = math.radians(angle)
            cartesian_point = (
                math.cos(angle_modifier * angle - math.pi / 2) * distance,
                math.sin(angle_modifier * angle - math.pi / 2) * distance
            )
            point = cartesian_to_screen(self.center, cartesian_point)
            if is_first_point:
                context.move_to(point[0], point[1])
                is_first_point = False
            else:
                context.line_to(int(point[0]), int(point[1]))

        r, g, b, a = stroke
        context.set_source_rgba(r, g, b, a)
        context.stroke_preserve()

        if fill is not None:
            r, g, b, a = fill
            context.set_source_rgba(r, g, b, a)
            context.fill()

    def _draw_legend(self, context: cairo.Context):
        if not self.settings.show_legend:
            return

        context.set_line_width(self.settings.theme.curve_line_width)

        context.new_path()
        context.set_dash(self.settings.theme.c0_dash)
        r, g, b, a = self.settings.theme.c0_stroke
        context.set_source_rgba(r, g, b, a)
        context.move_to(self.size - 100, self.size - 20)
        context.line_to(self.size - 100 + 15, self.size - 20)
        context.stroke()

        context.new_path()
        context.move_to(self.size - 100 + 18, self.size - 17)
        r, g, b, a = self.settings.theme.text_color
        context.set_source_rgba(r, g, b, a)
        context.show_text("C0-C180")
        context.stroke()

        context.new_path()
        context.set_dash(self.settings.theme.c180_dash)

        r, g, b, a = self.settings.theme.c180_stroke
        context.set_source_rgba(r, g, b, a)
        context.move_to(self.size - 100, self.size - 8)
        context.line_to(self.size - 100 + 15, self.size - 8)
        context.stroke()

        context.new_path()
        context.move_to(self.size - 100 + 18, self.size - 5)
        r, g, b, a = self.settings.theme.text_color
        context.set_source_rgba(r, g, b, a)
        context.show_text("C90-C270")
        context.stroke()
