import io

from gi.repository import Gio


def gio_file_stream(file: Gio.File):
    _, contents, _ = file.load_contents()
    return io.TextIOWrapper(io.BytesIO(contents), encoding="utf-8")