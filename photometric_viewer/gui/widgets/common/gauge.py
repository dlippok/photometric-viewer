from gi.repository.Gtk import Orientation, Box, Label, Expander, LevelBar

class Gauge(Box):
    def __init__(self, name: str, value: float, min_value: float, max_value: float, display=None, **kwargs):
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

        name_label = Label(label=name, hexpand=True, xalign=0)
        name_label.set_css_classes(["h1"])
        self.append(name_label)

        try:
            if min_value <= value <= max_value:
                level_bar = LevelBar(
                    min_value=min_value,
                    max_value=max_value,
                    value=value
                )
                self.append(level_bar)
        except ValueError:
            pass

        value_label = Label(label=display or value, hexpand=True, selectable=True)
        value_label.set_xalign(0)
        self.append(value_label)
