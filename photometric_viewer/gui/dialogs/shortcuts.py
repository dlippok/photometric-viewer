from gi.repository import Adw, Gtk

class ShortcutsWindow:
    def __init__(self, parent: Gtk.Window):
        self._window = Adw.ShortcutsDialog()
        self._parent = parent

        s = Adw.ShortcutsSection(title=_("Editing"))
        s.add(Adw.ShortcutsItem(title=_("Open file"), action_name="win.open"))
        s.add(Adw.ShortcutsItem(title=_("Save"), action_name="win.save"))
        s.add(Adw.ShortcutsItem(title=_("Save as"), action_name="win.save_as"))
        s.add(Adw.ShortcutsItem(title=_("Go to line"), action_name="win.goto_line"))
        s.add(Adw.ShortcutsItem(title=_("Show issues"), action_name="win.show_issues"))
        self._window.add(s)

        s = Adw.ShortcutsSection(title=_("Navigation"))
        s.add(Adw.ShortcutsItem(title=_("Go back"), action_name="win.nav.back"))
        s.add(Adw.ShortcutsItem(title=_("Go to top"), action_name="win.nav.top"))
        s.add(Adw.ShortcutsItem(title=_("Go to home page"), action_name="win.nav.home"))
        s.add(Adw.ShortcutsItem(title=_("Toggle sidebar"), action_name="win.toggle_sidebar"))
        self._window.add(s)

        s = Adw.ShortcutsSection()
        s.add(Adw.ShortcutsItem(title=_("Show light distribution curve"), action_name="win.show_ldc_zoom"))
        s.add(Adw.ShortcutsItem(title=_("Show photometric properties"), action_name="win.show_photometry"))
        s.add(Adw.ShortcutsItem(title=_("Show geometry"), action_name="win.show_geometry"))
        s.add(Adw.ShortcutsItem(title=_("Show intensity values"), action_name="win.show_intensity_values"))
        s.add(Adw.ShortcutsItem(title=_("Show direct ratios for room indices"), action_name="win.show_direct_ratios"))
        self._window.add(s)

        s = Adw.ShortcutsSection()
        s.add(Adw.ShortcutsItem(title=_("Export photometry"), action_name="win.export_photometry"))
        s.add(Adw.ShortcutsItem(title=_("Export light distribution curve"), action_name="win.export_photometry"))
        self._window.add(s)

        s = Adw.ShortcutsSection(title=_("Application"))
        s.add(Adw.ShortcutsItem(title=_("New window"), action_name="app.new_window"))
        s.add(Adw.ShortcutsItem(title=_("Preferences"), action_name="app.show_preferences"))
        s.add(Adw.ShortcutsItem(title=_("Keyboard shortcuts"), action_name="app.show_keyboard_shortcuts"))
        self._window.add(s)


    def show(self):
        self._window.present(self._parent)

