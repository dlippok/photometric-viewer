from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType, Orientation, SelectionMode

from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.photometry import Photometry


class IntensityValues(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.photometry = None
        self.selected_c_angle = None
        self.selected_gamma_angle = None

        self.property_list = PropertyList()
        self.selection_list = Gtk.ListBox()
        self.selection_list.set_selection_mode(SelectionMode.NONE)
        self.selection_list.set_css_classes(["boxed-list"])

        self.c_angle_selection_row = Adw.ComboRow()
        self.c_angle_selection_row.set_title(_("C Plane"))
        self.c_angle_selection_row.connect("notify::selected", self.on_update_c_angle)
        self.selection_list.append(self.c_angle_selection_row)

        self.gamma_angle_selection_row = Adw.ComboRow()
        self.gamma_angle_selection_row.set_title(_("Gamma angle"))
        self.gamma_angle_selection_row.connect("notify::selected", self.on_update_gamma_angle)
        self.selection_list.append(self.gamma_angle_selection_row)

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=32,
            margin_bottom=32,
            margin_start=32,
            margin_end=32
        )

        box.append(self.selection_list)
        box.append(self.property_list)

        clamp = Adw.Clamp()
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_child(scrolled_window)

    def set_photometry(self, photometry: Photometry):
        self.photometry = photometry
        self.selected_c_angle = photometry.c_planes[0]
        self.show_angle()

        c_angle_model = Gtk.StringList()
        c_angle_model.append(_("Show all"))
        for c_angle in self.photometry.c_planes:
            c_angle_model.append(str(c_angle))
        self.c_angle_selection_row.set_model(c_angle_model)

        gamma_angle_model = Gtk.StringList()
        gamma_angle_model.append(_("Show all"))
        for gamma_angle in self.photometry.gamma_angles:
            gamma_angle_model.append(str(gamma_angle))
        self.gamma_angle_selection_row.set_model(gamma_angle_model)

    def on_update_c_angle(self, *args):
        i = self.c_angle_selection_row.get_selected()
        if i == 0:
            self.selected_c_angle = None
        else:
            self.selected_c_angle = self.photometry.c_planes[i - 1]
        self.show_angle()

    def on_update_gamma_angle(self, *args):
        i = self.gamma_angle_selection_row.get_selected()
        if i == 0:
            self.selected_gamma_angle = None
        else:
            self.selected_gamma_angle = self.photometry.gamma_angles[i - 1]
        self.show_angle()

    def show_angle(self):
        self.property_list.clear()

        values = [
            (angle, v) for angle, v in self.photometry.intensity_values.items()
            if (self.selected_c_angle is None or angle[0] == self.selected_c_angle)
            and (self.selected_gamma_angle is None or angle[1] == self.selected_gamma_angle)
        ]

        if len(values) > 200:
            self.property_list.add(
                _("Too many values to display"),
                _("Select a particular C plane or gamma angle to display the values")
            )
            return

        unit = None
        match self.photometry.is_absolute:
            case True: unit = "cd"
            case False: unit = "cd/klm"

        for value in sorted(values, key=lambda v: v[0]):
            self.property_list.add(
                f"C: {value[0][0]}°, γ: {value[0][1]}°",
                f"{value[1]:.1f} {unit}"
            )
