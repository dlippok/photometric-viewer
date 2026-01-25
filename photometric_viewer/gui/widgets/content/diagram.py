import cairo
import math
from gi.repository.Gdk import RGBA
from gi.repository import Gtk, Adw
from gi.repository.Adw import AccentColor

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.config import plotter_themes
from photometric_viewer.utils.plotters import LightDistributionPlotter, DiagramStyle, SnapValueAnglesTo, \
    DisplayHalfSpaces, LightDistributionPlotterTheme
from photometric_viewer.utils.gi.GSettings import SettingsManager
from photometric_viewer.utils.coordinates import screen_to_cartesian


class PhotometricDiagram(Gtk.DrawingArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style_manager: Adw.StyleManager = Adw.StyleManager.get_default()
        self.style_manager.connect("notify", self.on_style_manager_notify)
        self.selected_theme = plotter_themes.THEMES[0]

        self.set_draw_func(self.on_draw)
        self.luminaire = None
        self.plotter = LightDistributionPlotter()

        self.settings_manager = SettingsManager()
        self.update_settings(self.settings_manager.settings)
        self.settings_manager.register_on_update(self.update_settings)


        move_controller = Gtk.EventControllerMotion()
        move_controller.connect('enter', self.on_mouse_enter)
        move_controller.connect('leave', self.on_mouse_left)
        move_controller.connect('motion', self.on_mouse_move)
        self.add_controller(move_controller)

    def on_draw(self, _, context: cairo.Context, width, height):
        if self.luminaire is None:
            return

        self.plotter.settings.show_legend = width > 220
        self.plotter.settings.show_values = width > 160

        self.set_content_height(width)
        self.set_name("photometric_diagram")
        self.plotter.size = width
        self.plotter.draw(context, self.luminaire)

    def set_photometry(self, luminaire: Luminaire):
        self.luminaire = luminaire
        if self.luminaire.intensity_values:
            self.set_visible(True)
            self.queue_draw()
        else:
            self.set_visible(False)

    def update_settings(self, settings: Settings):
        self.plotter.settings.style = DiagramStyle(settings.diagram_style.value)
        self.plotter.settings.snap_value_angles_to = SnapValueAnglesTo(settings.snap_value_angles_to.value)
        self.plotter.settings.display_half_spaces = DisplayHalfSpaces(settings.display_half_spaces.value)

        selected_theme = [theme for theme in plotter_themes.THEMES if theme.name == settings.diagram_theme]

        if selected_theme:
            self.selected_theme = selected_theme[0]
        else:
            self.selected_theme = plotter_themes.THEMES[0]

        self._update_high_contrast()
        self._update_plotter_theme()
        self.queue_draw()

    def _update_high_contrast(self):
        if self.selected_theme.is_high_contrast:
            return

        if self.style_manager.get_high_contrast():
            hc_themes = [theme for theme in plotter_themes.THEMES if theme.is_high_contrast]
            if hc_themes:
                self.selected_theme = hc_themes[0]

    def _update_plotter_theme(self):
        if self.style_manager.get_dark():
            theme = self.selected_theme.plotter_theme_dark
        else:
            theme = self.selected_theme.plotter_theme

        self._apply_accent_color(theme)
        self.plotter.settings.theme = theme

    def _apply_accent_color(self, theme: LightDistributionPlotterTheme):
        try:
            if self.selected_theme.use_system_accent_color:
                accent_color: AccentColor = self.style_manager.get_accent_color()
                rgba: RGBA = AccentColor.to_rgba(accent_color)

                theme.c0_fill = (rgba.red, rgba.green, rgba.blue, theme.c0_fill[3])
                theme.c0_stroke = (rgba.red, rgba.green, rgba.blue, rgba.alpha)
        except:
            return

    def _get_closest_gamma_angle(self, x, y):
        center = self.plotter.center
        cartesian = screen_to_cartesian(center, (x, y))
        angle = abs(math.atan2(cartesian[0], cartesian[1]) * 180 / math.pi)

        min_distance = 360
        closest_angle = None
        for luminaire_gamma in self.luminaire.gamma_angles:
            distance = abs(luminaire_gamma - angle)
            if distance < min_distance:
                closest_angle = luminaire_gamma
                min_distance = distance

        return closest_angle


    def on_style_manager_notify(self, *args):
        self._update_high_contrast()
        self._update_plotter_theme()
        self.queue_draw()

    def on_mouse_enter(self, motion, x, y):
        angle =self._get_closest_gamma_angle(x, y)
        self.plotter.highlight_angle = angle
        self.queue_draw()


    def on_mouse_move(self, motion, x, y):
        angle =self._get_closest_gamma_angle(x, y)
        self.plotter.highlight_angle = angle
        self.queue_draw()


    def on_mouse_left(self, _):
        self.plotter.highlight_angle = None
        self.queue_draw()
        
