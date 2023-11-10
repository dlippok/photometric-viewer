import copy
import math

from photometric_viewer.model.luminaire import Luminaire, LuminaireGeometry, Shape, LuminousOpeningGeometry, Lamps, \
    PhotometryMetadata, LuminaireType, LuminousOpeningShape, LuminairePhotometricProperties, Calculable
from photometric_viewer.model.units import LengthUnits

MINIMAL_LUMINAIRE = Luminaire(
    gamma_angles=[],
    c_planes=[],
    intensity_values={},
    photometry=LuminairePhotometricProperties(
        is_absolute=True,
        luminous_flux=Calculable(None),
        efficacy=Calculable(None),
        lor=Calculable(None),
        dff=Calculable(None)
    ),

    geometry=LuminaireGeometry(
        shape=Shape.RECTANGULAR,
        width=0.4,
        length=1.2,
        height=0.15
    ),
    luminous_opening_geometry=LuminousOpeningGeometry(
        shape=LuminousOpeningShape.ROUND,
        width=0.3,
        length=0.5,
        height=0.7,
        height_c90=0.8,
        height_c180=0.9,
        height_c270=1.0,
    ),
    lamps=[
        Lamps(
            number_of_lamps=1,
            description="Test lamp",
            catalog_number="LP1220",
            position="center",
            lumens_per_lamp=1200,
            wattage=80,
            color="6000K",
            cri="95",
            ballast_description="Test Ballast",
            ballast_catalog_number="BL2500"
        )
    ],
    metadata=PhotometryMetadata(
        luminaire="Test Luminaire",
        catalog_number="LM600",
        manufacturer="Test",
        additional_properties={
            "ADDITIONAL": "PROPERTY"
        },
        file_source="...",
        file_units=LengthUnits.METERS,
        luminaire_type=LuminaireType.LINEAR,
        measurement="MS123",
        date_and_user="2023-07-09",
        conversion_factor=1,
        filename="file.ldt"
    )
)

ABSOLUTE_PHOTOMETRY_LUMINAIRE = copy.deepcopy(MINIMAL_LUMINAIRE)
ABSOLUTE_PHOTOMETRY_LUMINAIRE.gamma_angles=[0, 45, 90]
ABSOLUTE_PHOTOMETRY_LUMINAIRE.c_planes=[0, 90, 180, 270]
ABSOLUTE_PHOTOMETRY_LUMINAIRE.intensity_values={
        (0, 0): 300,
        (0, 45): 100,
        (0, 90): 20,
        (90, 0): 300,
        (90, 45): 100,
        (90, 90): 20,
        (180, 0): 300,
        (180, 45): 100,
        (180, 90): 20,
        (270, 0): 300,
        (270, 45): 100,
        (270, 90): 20
}
ABSOLUTE_PHOTOMETRY_LUMINAIRE.photometry=LuminairePhotometricProperties(
        is_absolute=True,
        luminous_flux=Calculable(1200),
        efficacy=Calculable(None),
        lor=Calculable(100),
        dff=Calculable(100)
)

TWO_LAMPS_LUMINAIRE = copy.deepcopy(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
TWO_LAMPS_LUMINAIRE.is_absolute = False
TWO_LAMPS_LUMINAIRE.lamps = [
    Lamps(
        number_of_lamps=1,
        description="Test lamp 1",
        catalog_number="LP1221",
        position="center",
        lumens_per_lamp=1200,
        wattage=80,
        color="6000K",
        cri="95",
        ballast_description="Test Ballast",
        ballast_catalog_number="BL2501"
    ),
    Lamps(
        number_of_lamps=2,
        description="Test lamp 2",
        catalog_number="LP1222",
        position="center",
        lumens_per_lamp=1100,
        wattage=75,
        color="6500K",
        cri="90",
        ballast_description="Test Ballast 2",
        ballast_catalog_number="BL2502"
    ),
]

LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY = copy.deepcopy(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY.geometry = None

UNIFORM_RADIATING_SOURCE = copy.deepcopy(MINIMAL_LUMINAIRE)
UNIFORM_RADIATING_SOURCE.lamps[0].lumens_per_lamp = 1000 * 4 * math.pi
UNIFORM_RADIATING_SOURCE.c_planes = [0, 90, 180, 270]
UNIFORM_RADIATING_SOURCE.gamma_angles = [0, 30, 60, 90, 120, 150, 180]
UNIFORM_RADIATING_SOURCE.intensity_values = {
    (c, gamma): 1000
    for c in UNIFORM_RADIATING_SOURCE.c_planes
    for gamma in UNIFORM_RADIATING_SOURCE.gamma_angles
}

DOWNWARD_RADIATING_SOURCE = copy.deepcopy(UNIFORM_RADIATING_SOURCE)
DOWNWARD_RADIATING_SOURCE.intensity_values = {
    (c, gamma): (2000 if gamma < 90 else 0)
    for c in UNIFORM_RADIATING_SOURCE.c_planes
    for gamma in UNIFORM_RADIATING_SOURCE.gamma_angles
}

UPWARD_RADIATING_SOURCE = copy.deepcopy(UNIFORM_RADIATING_SOURCE)
UPWARD_RADIATING_SOURCE.intensity_values = {
    (c, gamma): (2000 if gamma >= 90 else 0)
    for c in UNIFORM_RADIATING_SOURCE.c_planes
    for gamma in UNIFORM_RADIATING_SOURCE.gamma_angles
}

NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE = copy.deepcopy(MINIMAL_LUMINAIRE)
NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.lamps[0].lumens_per_lamp = 1000 * 4 * math.pi
NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.c_planes = [0, 90, 180, 270]
NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.gamma_angles = [0, 10, 20, 30, 40, 50, 50, 70, 80, 90, 180]
NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.intensity_values = {
    (c, gamma): 1000
    for c in NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.c_planes
    for gamma in NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE.gamma_angles
}

NON_EQUIDISTANT_DOWNWARD_RADIATING_SOURCE = copy.deepcopy(NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE)
NON_EQUIDISTANT_DOWNWARD_RADIATING_SOURCE.intensity_values = {
    (c, gamma): (2000 if gamma < 90 else 0)
    for c in NON_EQUIDISTANT_DOWNWARD_RADIATING_SOURCE.c_planes
    for gamma in NON_EQUIDISTANT_DOWNWARD_RADIATING_SOURCE.gamma_angles
}

NON_EQUIDISTANT_UPWARD_RADIATING_SOURCE = copy.deepcopy(NON_EQUIDISTANT_UNIFORM_RADIATING_SOURCE)
NON_EQUIDISTANT_UPWARD_RADIATING_SOURCE.intensity_values = {
    (c, gamma): (2000 if gamma >= 90 else 0)
    for c in NON_EQUIDISTANT_UPWARD_RADIATING_SOURCE.c_planes
    for gamma in NON_EQUIDISTANT_UPWARD_RADIATING_SOURCE.gamma_angles
}

LOR_50_UNIFORM_RADIATING_SOURCE = copy.deepcopy(UNIFORM_RADIATING_SOURCE)
LOR_50_UNIFORM_RADIATING_SOURCE.photometry.is_absolute = False
LOR_50_UNIFORM_RADIATING_SOURCE.lamps = [
    Lamps(
        number_of_lamps=1,
        description="Test lamp",
        catalog_number="LP1220",
        position="center",
        lumens_per_lamp=2000,
    )
]
LOR_50_UNIFORM_RADIATING_SOURCE.c_planes = [0, 90, 180, 270]
LOR_50_UNIFORM_RADIATING_SOURCE.gamma_angles = [0, 30, 60, 90, 120, 150, 180]
LOR_50_UNIFORM_RADIATING_SOURCE.intensity_values = {
    (c, gamma): (1000/2) / (4 * math.pi)
    for c in LOR_50_UNIFORM_RADIATING_SOURCE.c_planes
    for gamma in LOR_50_UNIFORM_RADIATING_SOURCE.gamma_angles
}
