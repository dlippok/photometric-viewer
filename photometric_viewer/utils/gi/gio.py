import io

from gi.repository import Gio, GLib


def _detect_encoding(contents):
    wrapper = io.TextIOWrapper(io.BytesIO(contents), encoding="utf-8")
    try:
        wrapper.readline()
        return "utf-8"
    except UnicodeDecodeError:
        return "windows-1252"


def gio_file_stream(file: Gio.File):
    _, contents, _ = file.load_contents()
    encoding = _detect_encoding(contents)
    return io.TextIOWrapper(io.BytesIO(contents), encoding=encoding)

def write_string(file: Gio.File, data: str):
    stream: Gio.FileOutputStream = file.replace(None, False, Gio.FileCreateFlags.REPLACE_DESTINATION)
    data_as_bytes = GLib.Bytes(data=data.encode("utf-8"))
    stream.write_bytes(data_as_bytes)

def write_bytes(file: Gio.File, data: bytes):
    stream: Gio.FileOutputStream = file.replace(None, False, Gio.FileCreateFlags.REPLACE_DESTINATION)
    data_as_bytes = GLib.Bytes(data=data)
    stream.write_bytes(data_as_bytes)
