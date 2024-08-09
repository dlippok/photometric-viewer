from gi.repository import Gtk, Gdk
from gi.repository.Gtk import Box, Orientation, Label, Align
from gi.repository.Pango import WrapMode

from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.gui.widgets.content.header_buttons import HeaderButtons
from photometric_viewer.model.luminaire import Luminaire


class LuminaireHeader(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.HORIZONTAL,
            spacing=16,
        )

        self.set_homogeneous(True)
        self.diagram = PhotometricDiagram(
            vexpand=False,
            valign=Align.START
        )

        self.name_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,

            css_classes=["title-4"]

        )
        self.manufacturer_label = Label(
            xalign=0,
            hexpand=True,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes=["heading"]
        )
        self.description_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True
        )
        self.date_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes=["dim-label"]
        )

        self.measurement_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes=["dim-label"]
        )

        self.header_buttons = HeaderButtons()

        properties_box = Box(orientation=Orientation.VERTICAL, spacing=12)
        properties_box.append(self.name_label)
        properties_box.append(self.manufacturer_label)
        properties_box.append(self.date_label)
        properties_box.append(self.measurement_label)
        properties_box.append(self.description_label)
        properties_box.append(self.header_buttons)

        self.diagram_zoom_button = Gtk.Button(
            css_classes=["card"],
            valign=Gtk.Align.START,
            cursor=Gdk.Cursor.new_from_name("zoom-in"),
            child=self.diagram,
            visible=False,
            action_name="win.show_ldc_zoom"
        )

        self.append(self.diagram_zoom_button)
        self.append(properties_box)

    def set_photometry(self, luminaire: Luminaire):
        self.name_label.set_label(luminaire.metadata.catalog_number or _("No catalog number"))
        self.manufacturer_label.set_label(luminaire.metadata.manufacturer or _("No manufacturer"))
        self.description_label.set_label(luminaire.metadata.luminaire or _("No description"))
        self.date_label.set_label(luminaire.metadata.date_and_user or _("Measurement date unknown"))

        if luminaire.metadata.measurement:
            self.measurement_label.set_label(f'{_("Measurement")}: {luminaire.metadata.measurement}')
            self.measurement_label.set_visible(True)
        else:
            self.measurement_label.set_label("")
            self.measurement_label.set_visible(False)

        self.diagram.set_photometry(luminaire)
        self.header_buttons.set_photometry(luminaire)
        self.diagram_zoom_button.set_visible(luminaire.intensity_values)
