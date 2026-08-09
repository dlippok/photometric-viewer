import math

from photometric_viewer.model.luminaire import Luminaire, LuminairePhotometricProperties, Calculable
from photometric_viewer.profiling.decorators import profiled

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


def required_number_of_luminaires(flux_luminaire, mf, avg_illuminance, area):
    return math.ceil((avg_illuminance * area) / (flux_luminaire * mf))


def illuminance(flux_luminaire, mf, area):
    return flux_luminaire * mf / area


def empty_values():
    return LuminairePhotometricProperties(
        is_absolute=False,
        luminous_flux=Calculable(),
        lor=Calculable(),
        dff=Calculable(),
        efficacy=Calculable()
    )

class PhotometricPropertiesCalculator:
    def __init__(self):
        self.luminaire: Luminaire | None = None
        self.last_result: LuminairePhotometricProperties | None = None

    @profiled()
    def calculate(self, luminaire: Luminaire) -> LuminairePhotometricProperties:
        try:
            if self._needs_recalculation(luminaire):
                result = self._calculate_photometry(luminaire)
            else:
                result = self.last_result or self._calculate_photometry(luminaire)

            applied_result = LuminairePhotometricProperties(
                is_absolute=result.is_absolute,
                luminous_flux=luminaire.photometry.luminous_flux.to_calculated(result.luminous_flux.value),
                lor=luminaire.photometry.lor.to_calculated(result.lor.value),
                dff=luminaire.photometry.dff.to_calculated(result.dff.value),
                efficacy=luminaire.photometry.efficacy.to_calculated(result.efficacy.value)
            )

            self.last_result = result
            self.luminaire = luminaire
            return applied_result

        except Exception as e:
            return empty_values()

    def _needs_recalculation(self, luminaire: Luminaire):
        if self.luminaire is None:
            return True
        return any((
            luminaire.photometry.is_absolute != self.luminaire.photometry.is_absolute,
            luminaire.gamma_angles != self.luminaire.gamma_angles,
            luminaire.c_planes != self.luminaire.c_planes,
            luminaire.intensity_values != self.luminaire.intensity_values,
            luminaire.lamps[0] != self.luminaire.lamps[0]
        ))

    def _calculate_photometry(self, luminaire: Luminaire) -> LuminairePhotometricProperties:
        assert luminaire.intensity_values

        is_absolute = luminaire.photometry.is_absolute
        lamps = luminaire.lamps[0]
        ratio = 1 if is_absolute else (lamps.lumens_per_lamp * lamps.number_of_lamps) / 1000
        min_gamma = min(luminaire.gamma_angles)
        max_gamma = max(luminaire.gamma_angles)
        gamma_step = max(luminaire.gamma_angles[1] - luminaire.gamma_angles[0], 5)

        assert gamma_step > 0

        flux_luminaire = 0
        flux_lower_luminaire = 0
        for c in luminaire.c_planes:
            gamma = 0
            n = 1
            plane_flux = 0
            plane_lower_flux = 0
            while gamma < 180:
                if min_gamma <= gamma <= max_gamma :
                    closest_gamma = min(luminaire.gamma_angles, key=lambda x: abs(x - gamma))
                    candelas = luminaire.intensity_values.get((c, closest_gamma), 0) * ratio
                else:
                    candelas = 0
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
            luminous_flux=Calculable(flux_luminaire),
            lor=Calculable(lor),
            dff=Calculable(flux_lower_luminaire / flux_luminaire),
            efficacy=Calculable(efficacy)
        )

PHOTOMETRIC_PROPERTY_CALCULATOR = PhotometricPropertiesCalculator()