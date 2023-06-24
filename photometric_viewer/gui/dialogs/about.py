from gi.repository import Adw, Gtk


class AboutWindow:
    def __init__(self):
        self._about_window = Adw.AboutWindow(
            application_name="Photomertic Viewer",
            application_icon="io.github.dlippok.photometric-viewer",
            developer_name="Damian Lippok",
            version="1.0.1",
            website="https://github.com/dlippok/photometric-viewer",
            issue_url="https://github.com/dlippok/photometric-viewer/issues",
            copyright="© 2023 Damian Lippok",
            license_type=Gtk.License.MIT_X11
        )

    def show(self):
        self._about_window.show()
