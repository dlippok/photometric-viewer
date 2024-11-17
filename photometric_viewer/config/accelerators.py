from dataclasses import dataclass
from typing import List


@dataclass
class Accelerators:
    accelerators: List[str]
    action: str


ACCELERATORS = [
    Accelerators(accelerators=["<control>comma"], action="app.show_preferences"),
    Accelerators(accelerators=["<control>comma"], action="app.show_keyboard_shortcuts"),
    Accelerators(accelerators=["<control>o"], action="win.open"),
    Accelerators(accelerators=["<control>s"], action="win.save"),
    Accelerators(accelerators=["<shift><control>s"], action="win.save_as"),
    Accelerators(accelerators=["<control>u"], action="win.show_source"),
    Accelerators(accelerators=["<control>i"], action="win.show_intensity_values"),
    Accelerators(accelerators=["<alt>Left"], action="win.nav.back"),
    Accelerators(accelerators=["<alt>Up"], action="win.nav.top"),
    Accelerators(accelerators=["<alt>Home"], action="win.nav.home"),
    Accelerators(accelerators=["<control>n"], action="app.new_window"),
    Accelerators(accelerators=["<control>e"], action="win.export_photometry")
]
