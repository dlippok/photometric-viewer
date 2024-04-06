from dataclasses import dataclass
from typing import List


@dataclass
class Accelerators:
    accelerators: List[str]
    action: str


ACCELERATORS = [
    Accelerators(accelerators=["<control>comma"], action="app.show_preferences"),
    Accelerators(accelerators=["<control>comma"], action="app.show_keyboard_shortcuts"),
    Accelerators(accelerators=["<control>o"], action="app.open"),
    Accelerators(accelerators=["<control>s"], action="app.save"),
    Accelerators(accelerators=["<shift><control>s"], action="app.save_as"),
    Accelerators(accelerators=["<control>u"], action="app.show_source"),
    Accelerators(accelerators=["<control>i"], action="app.show_intensity_values"),
    Accelerators(accelerators=["<alt>Left"], action="app.nav.back"),
    Accelerators(accelerators=["<alt>Up"], action="app.nav.top"),
    Accelerators(accelerators=["<alt>Home"], action="app.nav.home")
]
