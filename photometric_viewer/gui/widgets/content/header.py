from gi.repository.Gtk import Box, Orientation, Label, Align
from gi.repository.Pango import WrapMode

from photometric_viewer.gui.widgets.content.diagram import PhotometricDiagram
from photometric_viewer.gui.widgets.content.header_buttons import HeaderButtons
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.model.settings import Settings


class LuminaireHeader(Box):
    def __init__(self):
        super().__init__(
            orientation=Orientation.HORIZONTAL,
            spacing=16,
        )

        self.set_homogeneous(True)
        self.diagram = PhotometricDiagram(
            vexpand=False,
            valign=Align.START,
            content_width=150
        )

        self.name_label = Label(
            xalign=0,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,

            css_classes=["title-2"]

        )
        self.manufacturer_label = Label(
            xalign=0,
            hexpand=True,
            wrap=True,
            wrap_mode=WrapMode.WORD_CHAR,
            selectable=True,
            css_classes=["title-3"]
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

        self.append(self.diagram)
        self.append(properties_box)

    def set_photometry(self, luminaire: Luminaire):
        self.name_label.set_label(luminaire.metadata.catalog_number or "")
        self.manufacturer_label.set_label(luminaire.metadata.manufacturer or "")
        self.description_label.set_label(luminaire.metadata.luminaire or "")
        self.date_label.set_label(luminaire.metadata.date_and_user or "")

        if luminaire.metadata.measurement:
            self.measurement_label.set_label(f'{_("Measurement")}: {luminaire.metadata.measurement}')
            self.measurement_label.set_visible(True)
        else:
            self.measurement_label.set_label("")
            self.measurement_label.set_visible(False)

        self.diagram.set_photometry(luminaire)
        self.header_buttons.set_photometry(luminaire)

    def update_settings(self, settings: Settings):
        self.diagram.update_settings(settings)

