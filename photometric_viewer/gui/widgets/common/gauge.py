from gi.repository.Gtk import Orientation, Box, Label, Expander, LevelBar
from gi.repository.Pango import WrapMode

from photometric_viewer.gui.widgets.common import badges


class Gauge(Box):
    def __init__(self, name: str, value: float, min_value: float, max_value: float, display=None, calculated: bool = False, hint: str | None = None, **kwargs):
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

        name_box = Box(orientation=Orientation.HORIZONTAL)
        name_label = Label(label=name, hexpand=True, xalign=0, wrap=True, wrap_mode=WrapMode.WORD_CHAR)
        name_label.set_css_classes(["h1"])
        name_box.append(name_label)

        if calculated:
            name_box.append(badges.calculated())

        self.append(name_box)

        if hint:
            hint_label = Label(
                label=hint,
                hexpand=True,
                xalign=0,
                wrap=True,
                wrap_mode=WrapMode.WORD_CHAR,
                selectable=True,
                css_classes=["dim-label"],
            )
            self.append(hint_label)


        try:
            bar_value = min(value, max_value)
            bar_value = max(bar_value, min_value)
            level_bar = LevelBar(
                min_value=min_value,
                max_value=max_value,
                value=bar_value,
                margin_top=8
            )
            self.append(level_bar)
        except ValueError:
            pass

        value_label = Label(label=display or value, hexpand=True, selectable=True)
        value_label.set_xalign(0)
        self.append(value_label)
