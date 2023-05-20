import io
from typing import IO

from gi.repository import Gio


def gio_file_stream(file: Gio.File):
    _, contents, _ = file.load_contents()
    return io.TextIOWrapper(io.BytesIO(contents), encoding="utf-8")


def read_non_empty_line(f: IO):
    line = f.readline()
    while line is not None:
        if line.strip() == "":
            line = f.readline()
            continue
        else:
            return line
