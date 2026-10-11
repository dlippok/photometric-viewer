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
            title="Gamma",
            subtitle=f"{gamma}°",
            title_selectable=True,
            subtitle_selectable=True,
            css_classes=["property"],
        )

        if locked:
            gamma_row.add_suffix(Gtk.Image(icon_name="value-lock-symbolic"))

        self.append(gamma_row)

        for angle, value in values.items():
            self.append(
                Adw.ActionRow(
                    title=f"C{angle}",
                    subtitle=f"{value:.0f} {unit}",
                    title_selectable=True,
                    subtitle_selectable=True,
                    css_classes=["property"],
                )
            )

