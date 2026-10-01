from typing import IO, List, Tuple

from photometry.iesna_common.model import MetadataTuple, InlineAttributes, LampAttributes, IesContent, \
    Attribute
from photometric_viewer.utils.ioutil import first_non_empty_line, get_n_values, read_till_end

def extract_content(f: IO) -> IesContent:
    header, curline = first_non_empty_line(f)
    metadata, curline = _extract_metadata(f, curline)
    inline_attributes, curline = _extract_inline_attributes(f, curline)
    lamp_attributes, curline = _extract_lamp_attributes(f, curline)

    v_angles = _extract_v_angles(f, inline_attributes, curline)
    if v_angles:
        curline = v_angles[-1].line

    h_angles = _extract_h_angles(f, inline_attributes, curline)
    if h_angles:
        curline = h_angles[-1].line

    intensities = _extract_intensities(f, curline)

    return IesContent(
        header=header,
        metadata=metadata,
        inline_attributes=inline_attributes,
        lamp_attributes=lamp_attributes,
        v_angles=v_angles,
        h_angles=h_angles,
        intensities=intensities,
    )


def _extract_metadata(f: IO, curline: int) -> Tuple[List[MetadataTuple], int]:
    metadata: List[MetadataTuple] = []

    next_line, n = first_non_empty_line(f)
    curline += n
    while next_line and next_line.startswith("["):
        metadata_line = next_line.split("]")
        metadata_key = metadata_line[0].strip("[")
        metadata_value = metadata_line[1].strip() if len(metadata_line) > 1 else ""
        t = MetadataTuple(metadata_key, metadata_value, curline)
        metadata.append(t)
        next_line, n = first_non_empty_line(f)
        curline += n

    return metadata, curline

def _extract_inline_attributes(f: IO, curline: int) -> tuple[InlineAttributes, int]:
    raw_values = get_n_values(f, 10)
    values = [Attribute(v[0], curline + v[1]) for v in raw_values]

    attributes = InlineAttributes(
        number_of_lamps=values[0],
        lumens_per_lamp=values[1],
        multiplying_factor=values[2],
        n_v_angles=values[3],
        n_h_angles=values[4],
        photometry_type=values[5],
        luminous_opening_units=values[6],
        luminous_opening_width=values[7],
        luminous_opening_length=values[8],
        luminous_opening_height=values[9]
    )

    return attributes, values[-1].line

def _extract_lamp_attributes(f: IO, curline: int) -> Tuple[LampAttributes, int]:
    raw_values = get_n_values(f, 3)
    values = [Attribute(v[0], curline + v[1]) for v in raw_values]

    attributes = LampAttributes(
        ballast_factor=values[0],
        ballast_lamp_photometric_factor=values[1],
        input_watts=values[2]
    )
    return attributes, values[-1].line


def _extract_v_angles(f: IO, attributes: InlineAttributes, curline: int) -> List[Attribute]:
    n_angles = attributes.n_v_angles
    if n_angles is None or n_angles.value is None:
        return []

    try:
        n_angles = int(n_angles.value)
        raw_angles = get_n_values(f, n_angles)
        return [Attribute(v[0], curline + v[1]) for v in raw_angles]

    except ValueError:
        return []


def _extract_h_angles(f: IO, attributes: InlineAttributes, curline: int) -> List[Attribute]:
    n_angles = attributes.n_h_angles
    if n_angles is None or n_angles.value is None:
        return []

    try:
        n_angles = int(n_angles.value)
        raw_angles = get_n_values(f, n_angles)
        return [Attribute(v[0], curline + v[1]) for v in raw_angles]

    except ValueError:
        return []


def _extract_intensities(f: IO, curline: int) -> List[Attribute]:
    raw_values = read_till_end(f)
    return [Attribute(v[0], curline + v[1]) for v in raw_values]
