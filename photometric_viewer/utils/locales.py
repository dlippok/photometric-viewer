import gettext
import locale
import os


def init_locale(application_id):
    locale_dir = "data/translations"
    locale.setlocale(locale.LC_ALL, '')

    if os.environ.get("container") == "flatpak":
        locale_dir = "/app/share/locale"

    elif (root := os.environ.get("SNAP")) and os.environ.get("SNAP_INSTANCE_NAME") == "photometric-viewer":
        locale_dir = root + "/share/locale"
        try:
            normalized_monetary = locale.normalize(locale.getlocale(locale.LC_MONETARY)[0])
            locale.setlocale(locale.LC_MONETARY, normalized_monetary)
        except locale.Error:
            pass

    locale.bindtextdomain(application_id, locale_dir)
    gettext.install(application_id, locale_dir)
