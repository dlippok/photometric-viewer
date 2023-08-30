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
