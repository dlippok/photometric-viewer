import math
from dataclasses import dataclass
from typing import List, Dict, Tuple

from photometric_viewer.model.photometry import Photometry, Lamps

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


@dataclass
class CalculatedPhotometricProperties:
    flux_luminaire: float
    lor: float
    dff: float


def calculate_photometric_properties(photometry: Photometry, lamps: Lamps):
    ratio = 1 if photometry.is_absolute else (lamps.lumens_per_lamp * lamps.number_of_lamps) / 1000
    gamma_step = photometry.gamma_angles[1] - photometry.gamma_angles[0]

    flux_luminaire = 0
    flux_lower_luminaire = 0
    for c in photometry.c_planes:
        gamma = 0
        n = 1
        plane_flux = 0
        plane_lower_flux = 0
        while gamma < 180:
            closest_gamma = min(photometry.gamma_angles, key=lambda x: abs(x - gamma))
            candelas = photometry.intensity_values.get((c, closest_gamma), 0) * ratio
            flux = candelas * (math.cos((n - 1) * math.radians(gamma_step)) - math.cos(n*math.radians(gamma_step)))
            plane_flux += flux
            if gamma < 90:
                plane_lower_flux += flux
            gamma += gamma_step
            n += 1
        flux_luminaire += plane_flux * 2 * math.pi / len(photometry.c_planes)
        flux_lower_luminaire += plane_lower_flux * 2 * math.pi / len(photometry.c_planes)

    lor = (flux_luminaire / (lamps.lumens_per_lamp * lamps.number_of_lamps)) if not photometry.is_absolute else 1

    return CalculatedPhotometricProperties(
        flux_luminaire=flux_luminaire,
        lor=lor,
        dff=flux_lower_luminaire / flux_luminaire
    )
