import json

from photometric_viewer.model.photometry import Photometry


def export_photometry(photometry: Photometry):
    luminaire_geometry = {
        "width": photometry.luminaire_geometry.width,
        "height": photometry.luminaire_geometry.height,
        "length": photometry.luminaire_geometry.length,
        "shape": photometry.luminaire_geometry.shape.name
    } if photometry.luminaire_geometry else None

    data = {
        "geometry": {
            "luminous_opening": {
                "shape": photometry.luminous_opening_geometry.shape.name,
                "width": photometry.luminous_opening_geometry.width,
                "length": photometry.luminous_opening_geometry.length,
                "height": photometry.luminous_opening_geometry.height,
                "height_c90": photometry.luminous_opening_geometry.height_c90,
                "height_c180": photometry.luminous_opening_geometry.height_c180,
                "height_c270": photometry.luminous_opening_geometry.height_c270,
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
        } for lamp_set in photometry.lamps],

        "photometry": {
            "dff": photometry.luminaire_photometric_properties.dff.value,
            "lorl": photometry.luminaire_photometric_properties.lor.value,
            "is_absolute": photometry.luminaire_photometric_properties.is_absolute,
            "c_planes": photometry.c_planes,
            "gamma_angles": photometry.gamma_angles,
            "values": [
                {
                    "c": coord[0],
                    "gamma": coord[1],
                    "value": value
                }
                for coord, value in photometry.intensity_values.items()
            ]
        },

        "metadata": {
            "luminaire": photometry.metadata.luminaire,
            "catalog_number": photometry.metadata.catalog_number,
            "manufacturer": photometry.metadata.manufacturer,
            "luminaire_type": photometry.metadata.luminaire_type.name if photometry.metadata.luminaire_type else None,
            "measurement": photometry.metadata.measurement,
            "date_and_user": photometry.metadata.date_and_user,
            "additional_properties": photometry.metadata.additional_properties
        }
    }
    return json.dumps(data, indent=4)
