from gi.repository import Adw
from gi.repository.Gtk import Button

from photometric_viewer.gui.widgets.app_menu import ApplicationMenuButton


def default_headerbar():
    open_button = Button(
        child=Adw.ButtonContent(label=_("Open"), icon_name="document-open-symbolic"),
        action_name="win.open"
    )

    header_bar = Adw.HeaderBar(css_classes=["flat"])
    header_bar.pack_start(open_button)

    header_bar.pack_end(ApplicationMenuButton())

    toggle_sidebar_button = Button(
        child=Adw.ButtonContent(icon_name="sidebar-show-right-symbolic"),
        action_name="win.toggle_sidebar"
    )
    header_bar.pack_end(toggle_sidebar_button)
    return header_bar

