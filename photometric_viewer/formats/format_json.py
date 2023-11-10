import json

from photometric_viewer.model.luminaire import Luminaire


def export_photometry(luminaire: Luminaire):
    luminaire_geometry = {
        "width": luminaire.geometry.width,
        "height": luminaire.geometry.height,
        "length": luminaire.geometry.length,
        "shape": luminaire.geometry.shape.name
    } if luminaire.geometry else None

    data = {
        "geometry": {
            "luminous_opening": {
                "shape": luminaire.luminous_opening_geometry.shape.name,
                "width": luminaire.luminous_opening_geometry.width,
                "length": luminaire.luminous_opening_geometry.length,
                "height": luminaire.luminous_opening_geometry.height,
                "height_c90": luminaire.luminous_opening_geometry.height_c90,
                "height_c180": luminaire.luminous_opening_geometry.height_c180,
                "height_c270": luminaire.luminous_opening_geometry.height_c270,
            },
            "luminaire": luminaire_geometry,
        },

        "lamp_sets": [{
            "number_of_lamps": lamp_set.number_of_lamps,
            "description": lamp_set.description,
            "catalog_number": lamp_set.catalog_number,
            "position": lamp_set.position,
            "lumens_per_lamp": lamp_set.lumens_per_lamp,
            "wattage": lamp_set.wattage,
            "color": lamp_set.color,
            "cri": lamp_set.cri,
            "ballast_description": lamp_set.ballast_description,
            "ballast_catalog_number": lamp_set.ballast_catalog_number
        } for lamp_set in luminaire.lamps],

        "photometry": {
            "dff": luminaire.photometry.dff.value,
            "lorl": luminaire.photometry.lor.value,
            "is_absolute": luminaire.photometry.is_absolute,
            "c_planes": luminaire.c_planes,
            "gamma_angles": luminaire.gamma_angles,
            "values": [
                {
                    "c": coord[0],
                    "gamma": coord[1],
                    "value": value
                }
                for coord, value in luminaire.intensity_values.items()
            ]
        },

        "metadata": {
            "luminaire": luminaire.metadata.luminaire,
            "catalog_number": luminaire.metadata.catalog_number,
            "manufacturer": luminaire.metadata.manufacturer,
            "luminaire_type": luminaire.metadata.luminaire_type.name if luminaire.metadata.luminaire_type else None,
            "measurement": luminaire.metadata.measurement,
            "date_and_user": luminaire.metadata.date_and_user,
            "additional_properties": luminaire.metadata.additional_properties
        }
    }
    return json.dumps(data, indent=4)
