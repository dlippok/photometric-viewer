from typing import IO, List

from photometric_viewer.photometry.ies95.model import MetadataTuple, InlineAttributes, LampAttributes, IesContent
from photometric_viewer.utils.conversion import safe_int, safe_float
from photometric_viewer.utils.ioutil import first_non_empty_line, get_n_values, read_till_end


def extract_content(f: IO) -> IesContent:
    header = _extract_header(f)
    metadata = _extract_metadata(f)
    inline_attributes = _extract_inline_attributes(f)
    lamp_attributes = _extract_lamp_attributes(f)
    v_angles = _extract_v_angles(f, inline_attributes)
    h_angles = _extract_h_angles(f, inline_attributes)
    intensities = _extract_intensities(f)

    return IesContent(
        header=header,
        metadata=metadata,
        inline_attributes=inline_attributes,
        lamp_attributes=lamp_attributes,
        v_angles=v_angles,
        h_angles=h_angles,
        intensities=intensities
    )


def _extract_header(f: IO) -> str | None:
    line = first_non_empty_line(f)
    if line is None:
        return None
    return line.strip()


def _extract_metadata(f: IO) -> List[MetadataTuple]:
    metadata = []
    next_line = first_non_empty_line(f)
    while next_line and next_line.startswith("["):
        metadata_line = next_line.split("]")
        metadata_key = metadata_line[0].strip("[").strip()
        metadata_value = metadata_line[1].strip()
        metadata.append(MetadataTuple(metadata_key, metadata_value))
        next_line = first_non_empty_line(f)
    return metadata


def _extract_inline_attributes(f: IO) -> InlineAttributes:
    raw_attributes = get_n_values(f, 10)
    return InlineAttributes(
        number_of_lamps=safe_int(raw_attributes[0]),
        lumens_per_lamp=safe_float(raw_attributes[1]),
        multiplying_factor=safe_float(raw_attributes[2]),
        n_v_angles=safe_int(raw_attributes[3]),
        n_h_angles=safe_int(raw_attributes[4]),
        photometry_type=safe_int(raw_attributes[5]),
        luminous_opening_units=safe_int(raw_attributes[6]),
        luminous_opening_width=safe_float(raw_attributes[7]),
        luminous_opening_length=safe_float(raw_attributes[8]),
        luminous_opening_height=safe_float(raw_attributes[9])
    )


def _extract_lamp_attributes(f: IO) -> LampAttributes:
    lamp_attr = get_n_values(f, 3)

    return LampAttributes(
        ballast_factor=safe_float(lamp_attr[0]),
        future_use=lamp_attr[1],
        input_watts=safe_float(lamp_attr[2])
    )


def _extract_v_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_v_angles or 0
    return [
        safe_float(angle)
        for angle in get_n_values(f, n_angles)
        if angle is not None
    ]


def _extract_h_angles(f: IO, attributes: InlineAttributes) -> List[float]:
    n_angles = attributes.n_h_angles or 0
    return [
        safe_float(angle)
        for angle in get_n_values(f, n_angles)
        if angle is not None
    ]


def _extract_intensities(f: IO) -> List[float]:
    return [
        safe_float(v)
        for v in read_till_end(f)
    ]
