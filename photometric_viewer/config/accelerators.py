from dataclasses import dataclass
from typing import List


@dataclass
class Accelerators:
    accelerators: List[str]
    action: str


ACCELERATORS = [
    Accelerators(accelerators=["<control>comma"], action="app.show_preferences"),
    Accelerators(accelerators=["<control>question"], action="app.show_keyboard_shortcuts"),
    Accelerators(accelerators=["<control>o"], action="win.open"),
    Accelerators(accelerators=["<control>s"], action="win.save"),
    Accelerators(accelerators=["<shift><control>s"], action="win.save_as"),
    Accelerators(accelerators=["<control>l"], action="win.show_ldc_zoom"),
    Accelerators(accelerators=["<control>i"], action="win.show_intensity_values"),
    Accelerators(accelerators=["<control>h"], action="win.show_photometry"),
    Accelerators(accelerators=["<control>m"], action="win.show_geometry"),
    Accelerators(accelerators=["<control>r"], action="win.show_direct_ratios"),
    Accelerators(accelerators=["F9"], action="win.toggle_sidebar"),
    Accelerators(accelerators=["<alt>Left"], action="win.nav.back"),
    Accelerators(accelerators=["<alt>Up"], action="win.nav.top"),
    Accelerators(accelerators=["<alt>Home"], action="win.nav.home"),
    Accelerators(accelerators=["<control>e"], action="win.export_photometry"),
    Accelerators(accelerators=["<shift><control>e"], action="win.export_ldc_as_image"),
    Accelerators(accelerators=["<shift><control>g"], action="win.goto_line"),
    Accelerators(accelerators=["<shift><control>i"], action="win.show_issues"),
    Accelerators(accelerators=["<control>w"], action="win.close"),
    Accelerators(accelerators=["<control>n"], action="app.new_window"),
]
