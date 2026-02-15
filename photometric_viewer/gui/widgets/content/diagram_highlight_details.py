from typing import Dict
from gi.repository import Gtk

class DiagramHighlightDetails(Gtk.Box):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_orientation(Gtk.Orientation.VERTICAL)

    def update(self, gamma: float, values: Dict[float, float], locked: bool, unit: str):
        child = self.get_first_child()

        while child is not None:
            self.remove(child)
            child = self.get_first_child()


        self.append(Gtk.Label(label=f"Gamma: {gamma}°"))
        if locked:
            self.append(Gtk.Label(label=f"Gamma: {gamma}°"))

        for angle, gamma in values.items():
            self.append(Gtk.Label(label=f"C{angle}: {gamma} {unit}"))


