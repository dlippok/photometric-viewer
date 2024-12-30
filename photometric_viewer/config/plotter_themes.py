from dataclasses import dataclass

from photometric_viewer.utils.plotters import LightDistributionPlotterTheme


@dataclass
class Theme:
    name: str
    plotter_theme: LightDistributionPlotterTheme
    plotter_theme_dark: LightDistributionPlotterTheme
    use_system_accent_color: bool = False
    is_high_contrast: bool = False


THEMES = [
    Theme(
        name="System",
        use_system_accent_color=True,
        is_high_contrast=True,
        plotter_theme=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(0, 0, 0, 0.8),
            curve_line_width=2,
            c0_stroke=(0x35/0xff, 0x84/0xff, 0xe4/0xff, 1),
            c0_fill=(0xfa/0xff, 0xfa/0xff, 0xfa/0xff, 0),
            c0_dash=[],
            c180_stroke=(0xf6/0xff, 0xd3/0xff, 0x2d/0xff, 1),
            c180_fill=(0xfa/0xff, 0xfa/0xff, 0xfa/0xff, 0),
            c180_dash=[],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(1, 1, 1, 1),
            curve_line_width=2,
            c0_stroke=(0x35/0xff, 0x84/0xff, 0xe4/0xff, 1),
            c0_fill=(0x38/0xff, 0x38/0xff, 0x38/0xff, 0),
            c0_dash=[],
            c180_stroke=(0xf6/0xff, 0xd3/0xff, 0x2d/0xff, 1),
            c180_fill=(0x38/0xff, 0x38/0xff, 0x38/0xff, 0),
            c180_dash=[],
        )
    ),
    Theme(
        name="Adwaita",
        plotter_theme=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(0, 0, 0, 0.8),
            curve_line_width=2,
            c0_stroke=(0x35/0xff, 0x84/0xff, 0xe4/0xff, 1),
            c0_fill=(0xfa/0xff, 0xfa/0xff, 0xfa/0xff, 0.6),
            c0_dash=[],
            c180_stroke=(0xf6/0xff, 0xd3/0xff, 0x2d/0xff, 1),
            c180_fill=(0xfa/0xff, 0xfa/0xff, 0xfa/0xff, 0.6),
            c180_dash=[],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(1, 1, 1, 1),
            curve_line_width=2,
            c0_stroke=(0x35/0xff, 0x84/0xff, 0xe4/0xff, 1),
            c0_fill=(0x38/0xff, 0x38/0xff, 0x38/0xff, 0.6),
            c0_dash=[],
            c180_stroke=(0xf6/0xff, 0xd3/0xff, 0x2d/0xff, 1),
            c180_fill=(0x38/0xff, 0x38/0xff, 0x38/0xff, 0.6),
            c180_dash=[],
        )
    ),
    Theme(
        name="Classic",
        plotter_theme=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[4],
            coordinate_color=(0.6, 0.6, 0.6, 1),
            text_color=(0.6, 0.6, 0.6, 1),
            curve_line_width=2,
            c0_stroke=(0.8, 0.8, 0, 0.4),
            c0_fill=(0.8, 0.8, 0, 0.2),
            c0_dash=[],
            c180_stroke=(0.8, 0.8, 0.0, 0.4),
            c180_fill=(0.8, 0.8, 0, 0.2),
            c180_dash=[2],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[4],
            coordinate_color=(0.6, 0.6, 0.6, 1),
            text_color=(0.6, 0.6, 0.6, 1),
            curve_line_width=2,
            c0_stroke=(0.8, 0.8, 0, 0.4),
            c0_fill=(0.8, 0.8, 0, 0.2),
            c0_dash=[],
            c180_stroke=(0.8, 0.8, 0.0, 0.4),
            c180_fill=(0.8, 0.8, 0, 0.2),
            c180_dash=[2],
        )
    ),
    Theme(
        name="Luxor",
        plotter_theme=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.8, 0.8, 0.8, 1),
            text_color=(0.0, 0.0, 0.0, 1),
            curve_line_width=1,
            c0_stroke=(1, 0.0, 0, 0.9),
            c0_fill=(1, 1, 0.4, 0.5),
            c0_dash=[],
            c180_stroke=(0, 0.0, 1, 0.9),
            c180_fill=(1, 1, 0.4, 0.5),
            c180_dash=[],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.8, 0.8, 0.8, 1),
            text_color=(1, 1, 1, 1),
            curve_line_width=1,
            c0_stroke=(1, 0.2, 0.2, 1),
            c0_fill=(1, 1, 0.4, 0.2),
            c0_dash=[],
            c180_stroke=(0.4, 0.4, 1, 1),
            c180_fill=(1, 1, 0.4, 0.2),
            c180_dash=[],
        )
    ),
    Theme(
        name="High Contrast",
        is_high_contrast=True,
        plotter_theme=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[1],
            coordinate_color=(0.5, 0.5, 0.5, 1),
            text_color=(0.0, 0.0, 0.0, 1),
            curve_line_width=2,
            c0_stroke=(0.2, 0.2, 0.2, 1),
            c0_fill=None,
            c0_dash=[],
            c180_stroke=(0.2, 0.2, 0.2, 1),
            c180_fill=None,
            c180_dash=[3],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=None,
            coordinate_line_width=1,
            coordinate_line_dash=[1],
            coordinate_color=(0.9, 0.9, 0.9, 1),
            text_color=(0.9, 0.9, 0.9, 1),
            curve_line_width=2,
            c0_stroke=(0.9, 0.9, 0.9, 1),
            c0_fill=None,
            c0_dash=[],
            c180_stroke=(0.9, 0.9, 0.9, 1),
            c180_fill=None,
            c180_dash=[3],
        ),
    ),

    Theme(
        name="Solarized",
        plotter_theme=LightDistributionPlotterTheme(
            background_color=(0.93, 0.96, 0.83, 1),
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(0.4, 0.4, 0.4, 1),
            curve_line_width=2,
            c0_stroke=(0.15, 0.55, 0.82, 1),
            c0_fill=(0.99, 0.96, 0.89, 0.5),
            c0_dash=[],
            c180_stroke=(0.71, 0.54, 0.0, 1),
            c180_fill=(0.99, 0.96, 0.89, 0.5),
            c180_dash=[],
        ),
        plotter_theme_dark=LightDistributionPlotterTheme(
            background_color=(0.0, 0.17, 0.21, 1),
            coordinate_line_width=1,
            coordinate_line_dash=[],
            coordinate_color=(0.5, 0.5, 0.5, 0.3),
            text_color=(0.4, 0.4, 0.4, 1),
            curve_line_width=2,
            c0_stroke=(0.15, 0.55, 0.82, 1),
            c0_fill=(0.03, 0.21, 0.26, 0.5),
            c0_dash=[],
            c180_stroke=(0.71, 0.54, 0.0, 1),
            c180_fill=(0.03, 0.21, 0.26, 0.5),
            c180_dash=[],
        )
    )
]
