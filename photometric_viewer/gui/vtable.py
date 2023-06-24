from gi.repository import Adw

from photometric_viewer.model.photometry import Photometry


class ValuesTable(Adw.Bin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def set_photometry(self, photometry: Photometry):
        pass