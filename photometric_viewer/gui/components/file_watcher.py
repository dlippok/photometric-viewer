import logging

from gi.repository import Gio, GLib, GObject


class FileWatcher(GObject.Object):
    __gsignals__ = {
        "file-changed": (
            GObject.SignalFlags.RUN_LAST,
            bool,
            (Gio.File,),
        ),
    }

    def __init__(self):
        super().__init__()
        self.file: Gio.File | None = None
        self.file_mtime: tuple[int, int] | None = None
        self.active = False
        GLib.timeout_add_seconds(1, self.check_file_mtime)

    def set_file(self, file: Gio.File | None):
        self.file = file
        self.refresh_file_mtime()

    def set_active(self, active: bool):
        self.active = active

    @staticmethod
    def get_file_mtime(file: Gio.File) -> tuple[int, int]:
        info = file.query_info(
            "time::modified,time::modified-usec",
            Gio.FileQueryInfoFlags.NONE,
            None,
        )
        modified = info.get_attribute_uint64("time::modified")
        modified_usec = (
            info.get_attribute_uint32("time::modified-usec")
            if info.has_attribute("time::modified-usec")
            else 0
        )
        return modified, modified_usec

    def refresh_file_mtime(self):
        if not self.file:
            self.file_mtime = None
            return

        try:
            self.file_mtime = self.get_file_mtime(self.file)
        except GLib.Error:
            self.file_mtime = None
            logging.exception("Could not query opened photometric file modification time")

    def check_file_mtime(self):
        if not self.file or not self.active:
            return GLib.SOURCE_CONTINUE

        try:
            file_mtime = self.get_file_mtime(self.file)
        except GLib.Error:
            logging.exception("Could not query opened photometric file modification time")
            return GLib.SOURCE_CONTINUE

        if self.file_mtime is not None and file_mtime != self.file_mtime:
            if self.emit("file-changed", self.file):
                self.file_mtime = file_mtime
        else:
            self.file_mtime = file_mtime

        return GLib.SOURCE_CONTINUE
