import math

from photometric_viewer.model.luminaire import Luminaire, Lamps, LuminairePhotometricProperties

DAYS_IN_YEAR = 365


def annual_power_consumption(wattage: float, daily_hours: float):
    if wattage < 0:
        raise ValueError("Wattage cannot be negative")

    if daily_hours > 24 or daily_hours < 0:
        raise ValueError("Daily hours must be between 0 and 24")

    return (wattage/1000) * daily_hours * DAYS_IN_YEAR


def energy_cost(power_consumption_kwh: float, price_kwh: float):
    if power_consumption_kwh < 0:
        raise ValueError("Power consumption cannot be negative")

    if price_kwh < 0:
        raise ValueError("Price per KWH cannot be negative")

    return power_consumption_kwh * price_kwh

def calculate_photometry(luminaire: Luminaire) -> LuminairePhotometricProperties:
    is_absolute = luminaire.photometry.is_absolute
    lamps = luminaire.lamps[0]
    ratio = 1 if is_absolute else (lamps.lumens_per_lamp * lamps.number_of_lamps) / 1000
    gamma_step = luminaire.gamma_angles[1] - luminaire.gamma_angles[0]

    flux_luminaire = 0
    flux_lower_luminaire = 0
    for c in luminaire.c_planes:
        gamma = 0
        n = 1
        plane_flux = 0
        plane_lower_flux = 0
        while gamma < 180:
            closest_gamma = min(luminaire.gamma_angles, key=lambda x: abs(x - gamma))
            candelas = luminaire.intensity_values.get((c, closest_gamma), 0) * ratio
            flux = candelas * (math.cos((n - 1) * math.radians(gamma_step)) - math.cos(n*math.radians(gamma_step)))
            plane_flux += flux
            if gamma < 90:
                plane_lower_flux += flux
            gamma += gamma_step
            n += 1
        flux_luminaire += plane_flux * 2 * math.pi / len(luminaire.c_planes)
        flux_lower_luminaire += plane_lower_flux * 2 * math.pi / len(luminaire.c_planes)

    lor = (flux_luminaire / (lamps.lumens_per_lamp * lamps.number_of_lamps)) if not is_absolute else 1
    efficacy = (flux_luminaire / lamps.wattage) if is_absolute and lamps.wattage else None

    return LuminairePhotometricProperties(
        is_absolute=luminaire.photometry.is_absolute,
        luminous_flux=luminaire.photometry.luminous_flux.to_calculated(flux_luminaire),
        lor=luminaire.photometry.lor.to_calculated(lor),
        dff=luminaire.photometry.dff.to_calculated(flux_lower_luminaire / flux_luminaire),
        efficacy=luminaire.photometry.efficacy.to_calculated(efficacy)
    )
