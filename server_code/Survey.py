import math
from datetime import datetime

import anvil.server
import anvil.users
from anvil.tables import app_tables


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

    if sleep is None or not 0 <= sleep <= 24:
        return {"ok": False, "message": "Enter sleep from 0 to 24 hours."}
    if weight is None or weight <= 0:
        return {"ok": False, "message": "Enter a weight greater than 0 kg."}
    if caffeine is None or caffeine < 0:
        return {"ok": False, "message": "Enter caffeine as 0 mg or more per day."}
    if height is None or height <= 0:
        return {"ok": False, "message": "Enter a height greater than 0 feet."}
    if meals is None or meals < 0 or not meals.is_integer():
        return {"ok": False, "message": "Enter meals per day as a whole number 0 or greater."}
    if quality is None or not quality.is_integer() or not 1 <= quality <= 10:
        return {"ok": False, "message": "Enter sleep quality as a whole number from 1 to 10."}

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
