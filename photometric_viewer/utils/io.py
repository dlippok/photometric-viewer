from typing import IO


def read_non_empty_line(f: IO):
    line = f.readline()
    while line is not None:
        if line.strip() == "":
            line = f.readline()
            continue
        else:
            return line
