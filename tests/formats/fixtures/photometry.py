import copy

from photometric_viewer.model.photometry import Photometry, LuminaireGeometry, Shape, LuminousOpeningGeometry, Lamps, \
    PhotometryMetadata, LuminaireType
from photometric_viewer.model.units import LengthUnits

ABSOLUTE_PHOTOMETRY_LUMINAIRE = Photometry(
    is_absolute=True,
    gamma_angles=[0, 45, 90],
    c_planes=[0, 90, 180, 270],
    intensity_values={
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
    },
    dff=100,
    lorl=100,
    luminaire_geometry=LuminaireGeometry(
        shape=Shape.RECTANGULAR,
        width=0.4,
        length=1.2,
        height=0.15
    ),
    luminous_opening_geometry=LuminousOpeningGeometry(
        shape=Shape.ROUND,
        width=0.3,
        length=0.5
    ),
    lamps=[
        Lamps(
            number_of_lamps=1,
            is_absolute=True,
            description="Test lamp",
            catalog_number="LP1220",
            position="center",
            lumens_per_lamp=1200,
            wattage=80,
            color="6000K",
            cri=95,
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

TWO_LAMPS_LUMINAIRE = copy.deepcopy(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
TWO_LAMPS_LUMINAIRE.is_absolute = False
TWO_LAMPS_LUMINAIRE.lamps = [
    Lamps(
        number_of_lamps=1,
        is_absolute=False,
        description="Test lamp 1",
        catalog_number="LP1221",
        position="center",
        lumens_per_lamp=1200,
        wattage=80,
        color="6000K",
        cri=95,
        ballast_description="Test Ballast",
        ballast_catalog_number="BL2501"
    ),
    Lamps(
        number_of_lamps=2,
        is_absolute=False,
        description="Test lamp 2",
        catalog_number="LP1222",
        position="center",
        lumens_per_lamp=1100,
        wattage=75,
        color="6500K",
        cri=90,
        ballast_description="Test Ballast 2",
        ballast_catalog_number="BL2502"
    ),
]

LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY = copy.deepcopy(ABSOLUTE_PHOTOMETRY_LUMINAIRE)
LUMINAIRE_WITHOUT_LUMINAIRE_GEOMETRY.luminaire_geometry = None