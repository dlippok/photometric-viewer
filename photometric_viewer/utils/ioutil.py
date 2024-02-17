from typing import IO


def read_non_empty_line(f: IO) -> str | None:
    line = f.readline()
    while line != "":
        if line.strip() == "":
            line = f.readline()
            continue
        else:
            return str(line.strip())
    return None


def get_n_values(f: IO, n: int):
    raw_values = []
    i = n
    while i > 0:
        line = read_non_empty_line(f)
        if line is None:
            values = [None] * i
        else:
            values = line.strip().split(" ")

        for value in values:
            if value == "":
                continue
            raw_values.append(value)
            i -= 1
    return raw_values[:n]

