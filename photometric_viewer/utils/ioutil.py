from typing import IO, Tuple


def first_non_empty_line(f: IO) -> Tuple[str | None, int]:
    line = f.readline()
    line_number = 1
    while line != "":
        if line.strip() == "":
            line = f.readline()
            line_number += 1
            continue
        else:
            return str(line.strip()), line_number
    return None, line_number


def read_line(f: IO) -> str | None:
    line = f.readline()
    if line == "":
        return None
    return line.strip()


def get_n_values(f: IO, n: int):
    raw_values = []
    i = n
    while i > 0:
        line, _ = first_non_empty_line(f)
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


def read_till_end(f: IO):
    raw_values = []
    line, _ = first_non_empty_line(f)
    while line is not None:
        values = line.strip().split(" ")
        for value in values:
            if value == "":
                continue
            raw_values.append(value)
        line, _ = first_non_empty_line(f)
    return raw_values