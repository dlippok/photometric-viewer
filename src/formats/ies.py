from typing import IO



def _get_n_values(f: IO, n: int):
    raw_values = []
    while n > 0:
        line = _read_non_empty_line(f)
        if line.strip() == "":
            continue

        values = line.strip().split(" ")
        for value in values:
            if value == "": continue
            raw_values.append(value)
            n -= 1
    return raw_values

def _read_non_empty_line(f: IO):
    line = f.readline()
    while line is not None:
        if line.strip() == "":
            line = f.readline()
            continue
        else:
            return line

def import_from_file(f: IO):
    ies_header = _read_non_empty_line(f)

    metadata = {}
    next_line = _read_non_empty_line(f)
    while next_line.startswith("["):
        metadata_line = next_line.split("]")
        metadata_key = metadata_line[0].strip("[").strip()
        metadata_value = metadata_line[1].strip()
        metadata[metadata_key] = metadata_value
        next_line = _read_non_empty_line(f)

    raw_attributes = _get_n_values(f, 10)
    attributes = {
        "numer_of_lamps": int(raw_attributes[0]),
        "lumens_per_lamp": float(raw_attributes[1]),
        "multiplying_factor": float(raw_attributes[2]),
        "n_v_angles": int(raw_attributes[3]),
        "n_h_angles": int(raw_attributes[4]),
        "luminous_opening_units": int(raw_attributes[5]),
        "luminous_opening_width": float(raw_attributes[6]),
        "luminous_opening_height": float(raw_attributes[7]),
        "luminous_opening_length": float(raw_attributes[8]),
    }

    [ballast_factor, lamp_photometric_factor, input_watts] = _get_n_values(f, 3)


    v_angles = [float(angle) for angle in _get_n_values(f, attributes["n_v_angles"])]
    h_angles = [float(angle) for angle in _get_n_values(f, attributes["n_h_angles"])]

    raw_values = _get_n_values(f, attributes["n_v_angles"] * attributes["n_h_angles"])

    candela_values = {}
    n = 0
    for h_angle in h_angles:
        for v_angle in v_angles:
            raw_value = float(raw_values[n])
            multiplying_factor = attributes["multiplying_factor"]
            value = raw_value * multiplying_factor * float(ballast_factor) * float(lamp_photometric_factor)
            candela_values[(h_angle, v_angle)] = value
            n += 1

    return Photometry(
        lumens=attributes["lumens_per_lamp"] * attributes["numer_of_lamps"] if attributes["lumens_per_lamp"] >= 0 else None,
        v_angles=v_angles,
        h_angles=h_angles,
        c_values=candela_values,
        metadata=PhotometryMetadata(
            luminaire=metadata.pop("LUMINAIRE", None),
            manufacturer=metadata.pop("MANUFAC", None),
            additional_properties=metadata
        )
    )

