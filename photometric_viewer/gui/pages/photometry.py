from cProfile import label

from gi.repository import Adw, Gtk
from gi.repository.Gtk import ScrolledWindow, PolicyType, Orientation

from photometric_viewer.config.appearance import CLAMP_MAX_WIDTH
from photometric_viewer.gui.pages.base import BasePage
from photometric_viewer.gui.widgets.common.gauge import Gauge
from photometric_viewer.gui.widgets.common.property_list import PropertyList
from photometric_viewer.model.luminaire import Luminaire
from photometric_viewer.utils import calc
from photometric_viewer.profiling.decorators import profiled


class PhotometryPage(BasePage):
    def __init__(self, **kwargs):
        super().__init__(_("Photometric Properties"), **kwargs)
        self.luminaire = None

        self.property_list = PropertyList()
        self.no_content_page = Adw.StatusPage(
            title=_("No content to display"),
            description=_("Photometric file doesn't contain any photometric properties"),
            icon_name='dialog-question',
            vexpand=True
        )

        box = Gtk.Box(
            orientation=Orientation.VERTICAL,
            spacing=16,
            margin_top=16,
            margin_bottom=16,
            margin_start=16,
            margin_end=16
        )

        box.append(self.property_list)
        box.append(self.no_content_page)

        clamp = Adw.Clamp(maximum_size=CLAMP_MAX_WIDTH)
        clamp.set_child(box)

        scrolled_window = ScrolledWindow()
        scrolled_window.set_child(clamp)
        scrolled_window.set_vexpand(True)
        scrolled_window.set_policy(PolicyType.NEVER, PolicyType.AUTOMATIC)
        self.set_content(scrolled_window)

    @profiled()
    def set_photometry(self, luminaire: Luminaire):
        if not self._needs_update(luminaire):
            return

        self.luminaire = luminaire
        self.property_list.clear()
        photometric_properties = calc.PHOTOMETRIC_PROPERTY_CALCULATOR.calculate(luminaire)

        has_content = False

        if photometric_properties.luminous_flux.value:
            self.property_list.add(
                _("Luminous flux"),
                f"{photometric_properties.luminous_flux.value:.0f}lm",
                is_calculated=photometric_properties.luminous_flux.is_calculated,
                hint=_("Total amount of light emitted by the luminaire.")
            )
            has_content = True

        if photometric_properties.lor.value:
            self.property_list.add(
                _("Light output ratio"),
                f"{photometric_properties.lor.value:.2%}",
                is_calculated=photometric_properties.lor.is_calculated,
                hint=_("Ratio of luminous flux emitted by the luminaire to the luminous flux emitted by the lamps.")
            )
            has_content = True

        if photometric_properties.efficacy.value:
            self.property_list.add(
                    _("Efficacy"),
                    f"{photometric_properties.efficacy.value:.0f}lm/w",
                    is_calculated=photometric_properties.efficacy.is_calculated,
                    hint=_("Ratio of luminous flux emitted by the luminaire to the power consumed by the luminaire.")
            )
            has_content = True

        if photometric_properties.dff.value:
            self.property_list.add(
                _("Downward flux fraction (DFF)"),
                f"{photometric_properties.dff.value:.0%}",
                is_calculated=photometric_properties.dff.is_calculated,
                hint=_(
                    "Ratio of luminous flux emitted by the luminaire in the downward hemisphere to the luminous flux "
                    "emitted by the luminaire in all directions."
                )
            )
            has_content = True

        self.property_list.set_visible(has_content)
        self.no_content_page.set_visible(not has_content)

    def _needs_update(self, luminaire: Luminaire):
        if luminaire and not self.luminaire:
            return True

        needs_update = any([
            luminaire.photometry != self.luminaire.photometry,
            luminaire.lamps != self.luminaire.lamps,
            luminaire.c_planes != self.luminaire.c_planes,
            luminaire.gamma_angles != self.luminaire.gamma_angles,
            luminaire.intensity_values != self.luminaire.intensity_values,
        ])

        return needs_update
