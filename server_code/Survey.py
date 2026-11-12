import math
from datetime import datetime

import anvil.server
import anvil.users
from anvil.tables import app_tables


WEIGHT_MIN_KG, WEIGHT_MAX_KG = 1, 500
TIMEZONE_MIN, TIMEZONE_MAX = -11, 12
BEDTIME_MIN, BEDTIME_MAX = 0, 23
SLEEP_QUALITY_MIN, SLEEP_QUALITY_MAX = 1, 10
CAFFEINE_SERVINGS_MIN, CAFFEINE_SERVINGS_MAX = 0, 50
MEALS_MIN, MEALS_MAX = 0, 20
TRAVEL_OPTIONS = {
    "1 - Never travel",
    "2 - Travel once every few years",
    "3 - Travel once or twice a year",
    "4 - Travel almost every month",
    "5 - Travel every day",
}


def _parse_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def _parse_integer(value):
    number = _parse_number(value)
    if number is None or not number.is_integer():
        return None
    return int(number)


def _parse_height_feet(value):
    text = str(value).strip()
    parts = text.split(".")
    if len(parts) not in (1, 2) or not parts[0].isdigit():
        return None
    feet = int(parts[0])
    inches_text = parts[1] if len(parts) == 2 else "0"
    if not inches_text.isdigit() or len(inches_text) > 2:
        return None
    inches = int(inches_text)
    if not 1 <= feet <= 8 or not 0 <= inches <= 11:
        return None
    return round(feet + inches / 12.0, 4)


@anvil.server.callable(require_user=True)
def save_survey(height_input, weight_value, weight_unit, timezone_offset,
                bedtime_hour, sleep_quality, travel_frequency,
                caffeine_servings_per_day, meals_per_day):
    height_feet = _parse_height_feet(height_input)
    if height_feet is None:
        return {"ok": False, "message": "Enter height as feet.inches, from 1.0 to 8.11."}

    weight = _parse_number(weight_value)
    unit = str(weight_unit).lower()
    if weight is None or unit not in ("kg", "lb"):
        return {"ok": False, "message": "Choose kg or lb and enter a valid weight."}
    weight_kg = weight if unit == "kg" else weight * 0.453592
    if not WEIGHT_MIN_KG <= weight_kg <= WEIGHT_MAX_KG:
        return {"ok": False, "message": "Weight must be between 1 and 500 kg, or the equivalent in pounds."}

    timezone = _parse_integer(timezone_offset)
    if timezone is None or not TIMEZONE_MIN <= timezone <= TIMEZONE_MAX:
        return {"ok": False, "message": "Time zone must be a whole-hour offset from -11 to +12."}

    bedtime = _parse_integer(bedtime_hour)
    if bedtime is None or not BEDTIME_MIN <= bedtime <= BEDTIME_MAX:
        return {"ok": False, "message": "Bedtime must be a whole number from 0 to 23."}

    quality = _parse_integer(sleep_quality)
    if quality is None or not SLEEP_QUALITY_MIN <= quality <= SLEEP_QUALITY_MAX:
        return {"ok": False, "message": "Sleep quality must be a whole number from 1 to 10."}

    travel = str(travel_frequency)
    if travel not in TRAVEL_OPTIONS:
        return {"ok": False, "message": "Choose one of the listed travel options."}

    caffeine_servings = _parse_integer(caffeine_servings_per_day)
    if (caffeine_servings is None
            or not CAFFEINE_SERVINGS_MIN <= caffeine_servings <= CAFFEINE_SERVINGS_MAX):
        return {"ok": False, "message": "Caffeine servings must be a whole number from 0 to 50 per day."}

    meals = _parse_integer(meals_per_day)
    if meals is None or not MEALS_MIN <= meals <= MEALS_MAX:
        return {"ok": False, "message": "Meals must be a whole number from 0 to 20 per day."}

    user = anvil.users.get_user()
    app_tables.survey_responses.add_row(
        user=user,
        height_feet=height_feet,
        weight_Kg=round(weight_kg, 2),
        weight_input_unit=unit,
        timezone_offset=timezone,
        bedtime_hour=bedtime,
        sleep_quality=quality,
        travel_frequency=travel,
        caffeine_servings_per_day=caffeine_servings,
        meals_per_day=meals,
        submitted_at=datetime.now(),
    )
    return {"ok": True}
