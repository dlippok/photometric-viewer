from gi.repository import Adw, Gtk

from photometric_viewer.utils.project import PROJECT


class AboutWindow:
    def __init__(self):
        self._about_window = Adw.AboutWindow(
            application_name=_(PROJECT.name),
            application_icon=PROJECT.id,
            developer_name=PROJECT.developer_name,
            version=PROJECT.version,
            website=PROJECT.urls.homepage,
            issue_url=PROJECT.urls.bug_tracker,
            support_url=PROJECT.urls.support,
            copyright=PROJECT.copyright,
            license_type=Gtk.License.MIT_X11
        )

    def show(self):
        self._about_window.show()
