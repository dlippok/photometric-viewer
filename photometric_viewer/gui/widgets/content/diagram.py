import cairo
from gi.repository import Gtk, Adw

from photometric_viewer.model.settings import Settings
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.config import plotter_themes
from photometric_viewer.utils.plotters import LightDistributionPlotter, DiagramStyle, SnapValueAnglesTo, \
    DisplayHalfSpaces
from photometric_viewer.utils.gi.GSettings import SettingsManager


class PhotometricDiagram(Gtk.DrawingArea):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.style_manager: Adw.StyleManager = Adw.StyleManager.get_default()
        self.style_manager.connect("notify", self.on_style_manager_notify)
        self.selected_theme = plotter_themes.THEMES[0]

        self.set_css_classes(["boxed-list"])
        self.set_draw_func(self.on_draw)
        self.luminaire = None
        self.plotter = LightDistributionPlotter()

        self.settings_manager = SettingsManager()
        self.update_settings(self.settings_manager.settings)
        self.settings_manager.register_on_update(self.update_settings)

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
        self._update_plotter_theme()

        self.queue_draw()

    def _update_plotter_theme(self):
        if self.style_manager.get_dark():
            self.plotter.settings.theme = self.selected_theme.plotter_theme_dark
        else:
            self.plotter.settings.theme = self.selected_theme.plotter_theme

    def on_style_manager_notify(self, *args):
        self._update_plotter_theme()
        self.queue_draw()