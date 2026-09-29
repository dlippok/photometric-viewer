from typing import IO, Tuple, List


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


def get_n_values(f: IO, n: int) -> List[Tuple[str, int]]:
    raw_values = []
    i = n
    line_number = 0
    while i > 0:
        line, read_lines = first_non_empty_line(f)
        line_number += read_lines
        if line is None:
            values = [None] * i
        else:
            values = line.strip().split(" ")

        for value in values:
            if value == "":
                continue
            raw_values.append((value, line_number))
            i -= 1
    return raw_values[:n]


def read_till_end(f: IO) -> List[Tuple[str, int]]:
    raw_values = []
    line, line_number = first_non_empty_line(f)
    while line is not None:
        values = line.strip().split(" ")
        for value in values:
            if value == "":
                continue
            raw_values.append((value, line_number))
        line, read_lines = first_non_empty_line(f)
        line_number += read_lines
    return raw_values