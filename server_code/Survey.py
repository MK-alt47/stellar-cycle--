import math
from datetime import datetime

import anvil.server
import anvil.users
from anvil.tables import app_tables

SLEEP_MIN, SLEEP_MAX = 0, 24
WEIGHT_MIN_KG, WEIGHT_MAX_KG = 1, 500
CAFFEINE_MIN_MG, CAFFEINE_MAX_MG = 0, 2000
HEIGHT_MIN_FEET, HEIGHT_MAX_FEET = 1, 8
MEALS_MIN, MEALS_MAX = 0, 20
SLEEP_QUALITY_MIN, SLEEP_QUALITY_MAX = 1, 10


def _parse_number(value):
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


@anvil.server.callable(require_user=True)
def save_survey(sleep_hours, weight_kg, caffeine_mg_per_day, height_feet,
                meals_per_day, sleep_quality):
    sleep = _parse_number(sleep_hours)
    weight = _parse_number(weight_kg)
    caffeine = _parse_number(caffeine_mg_per_day)
    height = _parse_number(height_feet)
    meals = _parse_number(meals_per_day)
    quality = _parse_number(sleep_quality)

    if sleep is None or not SLEEP_MIN <= sleep <= SLEEP_MAX:
        return {"ok": False, "message": "Hours of sleep must be between 0 and 24."}
    if weight is None or not WEIGHT_MIN_KG <= weight <= WEIGHT_MAX_KG:
        return {"ok": False, "message": "Weight must be between 1 and 500 kg."}
    if caffeine is None or not CAFFEINE_MIN_MG <= caffeine <= CAFFEINE_MAX_MG:
        return {"ok": False, "message": "Caffeine must be between 0 and 2,000 mg per day."}
    if height is None or not HEIGHT_MIN_FEET <= height <= HEIGHT_MAX_FEET:
        return {"ok": False, "message": "Height must be between 1 and 8 feet."}
    if meals is None or not MEALS_MIN <= meals <= MEALS_MAX or not meals.is_integer():
        return {"ok": False, "message": "Meals per day must be a whole number from 0 to 20."}
    if (quality is None or not quality.is_integer()
            or not SLEEP_QUALITY_MIN <= quality <= SLEEP_QUALITY_MAX):
        return {"ok": False, "message": "Sleep quality must be a whole number from 1 to 10."}

    user = anvil.users.get_user()
    app_tables.survey_responses.add_row(
        user=user,
        sleep_hours=sleep,
        weight_Kg=weight,
        caffeine_mg_per_day=caffeine,
        height_feet=height,
        meals_per_day=int(meals),
        sleep_quality=int(quality),
        submitted_at=datetime.now(),
    )
    return {"ok": True}
