from gi.repository.Gtk import Orientation, Box, Label, Expander, Justification
from gi.repository.Pango import WrapMode


class ColorTemperatureGauge(Box):
    def __init__(self, color_temperature: int, **kwargs):
        super().__init__(
            orientation=Orientation.VERTICAL,
            homogeneous=False,
            spacing=4,
            margin_start=16,
            margin_end=16,
            margin_top=16,
            margin_bottom=16,
            **kwargs
        )

        self.LIGHT_SOURCES = [
            (1600, 1799, _("Low Pressure Sodium Lamp"), "1700 K"),
            (1800, 2200, _("Sodium Lamp"), "2000 K"),
            (2550, 2649, _("Incandescent lamp 40 W"), "2600 K"),
            (2650, 2749, _("Incandescent lamp 60 W"), "2700 K"),
            (2750, 2849, _("Incandescent lamp 100 W"), "2800 K"),
            (2850, 3099, _("Warm white compact fluorescent and LED lamps"), "3000 K"),
            (3100, 3299, _("Halogen incandescent lamp"), "3200 K"),
            (3300, 3399, _("Studio CP light"), "3350 K"),
            (3800, 4200, _("Neutral white fluorescent lamp"), "4000 K"),
            (4800, 5249, _("Sunrise/Sunset"), "5000 K"),
            (5250, 5699, _("Morning/Afternoon"), "5500 K"),
            (5700, 5999, _("Noon"), "5800 K"),
            (6000, 6299, _("Xenon lamp"), "6200 K"),
            (6300, 6800, _("Overcast sky"), "6500 K")
        ]

        self.color_temperature = color_temperature

        name_label = Label(label=_("Color temperature"), hexpand=True, xalign=0)
        name_label.set_css_classes(["h1"])
        self.append(name_label)

        self.color_temperature_label = Label(hexpand=True, selectable=True)
        self.color_temperature_label.set_xalign(0)
        self.append(self.color_temperature_label)

        self.temp_bar = Label(css_classes=["temperature-bar"], label="|")
        self.append(self.temp_bar)

        label_box = Box(orientation=Orientation.HORIZONTAL, homogeneous=True)
        label_box.append(Label(
            label=_("Warm White\n(< 3300 K)"),
            xalign=0,
            css_classes=["dim-label", "small"],
            justify=Justification.LEFT
        ))

        label_box.append(Label(
            label=_("Neutral White\n(3300 K ... 5300 K)"),
            xalign=0.5,
            css_classes=["dim-label", "small"],
            justify=Justification.CENTER
        ))

        label_box.append(Label(
            label=_("Cold White\n(> 5300 K)"),
            xalign=1,
            css_classes=["dim-label", "small"],
            justify=Justification.RIGHT
        ))

        self.append(label_box)

        closest_temperature_box = Box(orientation=Orientation.HORIZONTAL)
        self.closest_source_label = Label(label="", selectable=True, margin_top=8, wrap=True, wrap_mode=WrapMode.WORD_CHAR)
        closest_temperature_box.append(self.closest_source_label)

        self.append(closest_temperature_box)

        sources_expander = Expander(label=_("Common light temperatures"), margin_top=8)

        similar_sources_box = Box(orientation=Orientation.VERTICAL)
        for source in self.LIGHT_SOURCES:
            similar_source_box = Box(
                orientation=Orientation.HORIZONTAL,
                margin_top=4,
                margin_start=12,
                margin_end=12
            )
            similar_source_box.append(
                Label(
                    label=source[2],
                    hexpand=True,
                    xalign=0,
                    wrap=True,
                    wrap_mode=WrapMode.WORD_CHAR,
                    selectable=True,
                    margin_end=6,
                )
            )
            similar_source_box.append(Label(label=source[3], xalign=1, selectable=True))
            similar_sources_box.append(similar_source_box)
        sources_expander.set_child(similar_sources_box)

        self.append(sources_expander)

        self.update()

    def _get_closest_source(self, temperature):
        for source in self.LIGHT_SOURCES:
            if source[0] <= temperature <= source[1]:
                return source
        return None

    def update(self):
        self.color_temperature_label.set_label(f"{self.color_temperature} K")
        position = 0
        match self.color_temperature:
            case x if x < 1600:
                position = 0
            case x if 1600 <= x < 6800:
                position = (x-1600)/(6800-1600)
            case x if x >= 6800:
                position = 1

        self.color_temperature_label.set_xalign(position)
        self.temp_bar.set_xalign(position)

        closest_source = self._get_closest_source(self.color_temperature)
        if closest_source:
            self.closest_source_label.set_label(_("Similar to: {} ({})").format(closest_source[2], closest_source[3]))
        else:
            self.closest_source_label.set_label("")

