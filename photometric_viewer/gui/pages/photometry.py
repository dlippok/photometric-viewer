from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType, Orientation

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils import calc


class PhotometryPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Photometric Properties"), **kwargs)
        self.luminaire = None

        self.property_list = PropertyList()

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=50,
            margin_bottom=50,
            margin_start=16,
            margin_end=16
        )

        box.append(self.property_list)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    def set_photometry(self, luminaire: Luminaire):
        self.property_list.clear()
        photometric_properties = calc.calculate_photometry(luminaire)

        if photometric_properties.luminous_flux.value:
            self.property_list.add(
                _("Luminous flux"),
                f"{photometric_properties.luminous_flux.value:.0f}lm",
                is_calculated=photometric_properties.luminous_flux.is_calculated,
                hint=_("Total amount of light emitted by the luminaire.")
            )

        if photometric_properties.lor.value:
            self.property_list.append(
                Gauge(
                    name=_("Light output ratio"),
                    value=photometric_properties.lor.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.lor.value:.2%}",
                    calculated=photometric_properties.lor.is_calculated,
                    hint=_("Ratio of luminous flux emitted by the luminaire to the luminous flux emitted by the lamps.")
                )
            )

        if photometric_properties.efficacy.value:
            self.property_list.append(Gauge(
                name=_("Efficacy"),
                min_value=0, max_value=160,
                value=photometric_properties.efficacy.value,
                display=f"{photometric_properties.efficacy.value:.0f}lm/w",
                calculated=photometric_properties.efficacy.is_calculated,
                hint=_("Ratio of luminous flux emitted by the luminaire to the power consumed by the luminaire.")
            ))

        if photometric_properties.dff.value:
            self.property_list.append(
                Gauge(
                    name=_("Downward flux fraction (DFF)"),
                    value=photometric_properties.dff.value,
                    min_value=0,
                    max_value=1,
                    display=f"{photometric_properties.dff.value:.0%}",
                    calculated=photometric_properties.dff.is_calculated,
                    hint=_(
                        "Ratio of luminous flux emitted by the luminaire in the downward hemisphere to the luminous flux emitted by the luminaire in all directions.")
                )
            )