from typing import Dict
from gi.repository import Gtk, Adw

class DiagramHighlightDetails(Gtk.ListBox):
    def __init__(self, **kwargs):
        super().__init__(css_classes=['boxed-list'], selection_mode=Gtk.SelectionMode.NONE, **kwargs)

    def update(self, gamma: float, values: Dict[float, float], locked: bool, unit: str):
        child = self.get_first_child()

        while child is not None:
            self.remove(child)
            child = self.get_first_child()


        gamma_row = Adw.ActionRow(
            title=f"{gamma}°",
            subtitle="Gamma",
            title_selectable=True,
            subtitle_selectable=True,
        )

        if locked:
            gamma_row.add_suffix(Gtk.Label(label=_("Locked")))

        self.append(gamma_row)

        for angle, value in values.items():
            self.append(
                Adw.ActionRow(
                    title=f"{value:.0f} {unit}",
                    subtitle=f"C{angle}",
                    title_selectable=True,
                    subtitle_selectable=True,
                )
            )

