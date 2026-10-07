from gi.repository import Gtk, Gdk
from gi.repository.Gtk import Box, Orientation, Label, Align
from gi.repository.Pango import WrapMode

from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.profiling.decorators import profiled


class LuminaireHeader(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.VERTICAL,
            spacing=16,
        )

        top_box = Gtk.Box(
            orientation=Orientation.HORIZONTAL,
            spacing=16,
        )

        self.diagram = PhotometricDiagram(
            show_values_under_cursor=False,
            vexpand=False,
            valign=Align.START
        )

        self.diagram_zoom_button = Gtk.Button(
            css_classes=["card"],
            valign=Gtk.Align.START,
            cursor=Gdk.Cursor.new_from_name("zoom-in"),
            child=self.diagram,
            visible=False,
            action_name="win.show_ldc_zoom",
            width_request=150
        )

        self.catalog_number_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,

        )
        self.catalog_number_row = self._label_with_icon('catalog-number-symbolic', self.catalog_number_label)

        self.manufacturer_label = Label(
            xalign=0,
            hexpand=True,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
        )
        self.manufacturer_row = self._label_with_icon('manufacturer-symbolic', self.manufacturer_label)

        self.name_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes = ["title-3"]
        )

        self.date_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True
        )
        self.date_row = self._label_with_icon('date-symbolic', self.date_label)

        self.measurement_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True
        )
        self.measurement_row = self._label_with_icon('measurement-symbolic', self.measurement_label)

        self.description_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes=['body']
        )

        properties_box = Box(orientation=Orientation.VERTICAL, spacing=12)

        properties_box.append(self.name_label)
        properties_box.append(self.catalog_number_row)
        properties_box.append(self.manufacturer_row)
        properties_box.append(self.measurement_row)
        properties_box.append(self.date_row)

        top_box.append(self.diagram_zoom_button)
        top_box.append(properties_box)

        self.append(top_box)
        self.append(self.description_label)

    @profiled()
    def set_photometry(self, luminaire: Luminaire):
        self.name_label.set_label(luminaire.metadata.luminaire or _("No description"))
        self.catalog_number_label.set_label(luminaire.metadata.catalog_number or _("No catalog number"))
        self.manufacturer_label.set_label(luminaire.metadata.manufacturer or _("No manufacturer"))

        if luminaire.metadata.date_and_user:
            self.date_label.set_label(luminaire.metadata.date_and_user)
            self.date_row.set_visible(True)
        else:
            self.date_label.set_label("")
            self.date_row.set_visible(False)

        if luminaire.metadata.measurement:
            self.measurement_label.set_label(luminaire.metadata.measurement)
            self.measurement_row.set_visible(True)
        else:
            self.measurement_label.set_label("")
            self.measurement_row.set_visible(False)

        if luminaire.metadata.description:
            self.description_label.set_label(luminaire.metadata.description)
            self.description_label.set_visible(True)
        else:
            self.description_label.set_label("")
            self.description_label.set_visible(False)

        self.diagram.set_photometry(luminaire)
        self.diagram_zoom_button.set_visible(luminaire.intensity_values)

    def _label_with_icon(self, icon_name: str, label: Label) -> Box:
        box = Box(orientation=Orientation.HORIZONTAL, spacing=6)
        box.append(Gtk.Image(icon_name=icon_name, valign=Gtk.Align.START))
        box.append(label)
        return box
