import anvil.server
import anvil.users
from anvil.tables import app_tables


CAFFEINE_DAILY_MAX = 3


def _caffeine_target(servings, sleep_quality, meals_per_day):
    if servings in (1, 2):
        target = 3
    elif servings in (3, 4):
        target = servings
    elif servings > 4:
        target = 3
    else:
        target = 0

    if sleep_quality <= 2:
        target -= 2

    if meals_per_day == 0:
        target += 1
    elif meals_per_day in (2, 3):
        target -= 1

    return max(0, min(CAFFEINE_DAILY_MAX, target))


def _caffeine_times(servings, target, sleep_quality, meals_per_day):
    times = set()
    if servings in (1, 2) or servings > 4 or target != servings:
        times.add("10:00")
    if sleep_quality <= 2:
        times.add("11:00")
    if meals_per_day <= 3:
        times.update(("10:00", "20:00"))

    if not times:
        return "Ongoing"

    return ", ".join(sorted(times)) + " UTC"


def _caffeine_action(current_servings, target, sleep_quality, meals_per_day):
    change = target - current_servings
    if change > 0:
        action = "Increase by {} to {} servings total per day.".format(change, target)
    elif change < 0:
        action = "Reduce by {} to {} servings total per day.".format(-change, target)
    else:
        action = "Maintain {} servings total per day.".format(target)

    adjustments = []
    if sleep_quality <= 2:
        adjustments.append("the sleep-score reduction")
    if meals_per_day == 0:
        adjustments.append("the meals-based increase")
    elif meals_per_day in (2, 3):
        adjustments.append("the meals-based reduction")

    if adjustments:
        action += " This target combines {} and is capped at 3 servings per day.".format(
            " and ".join(adjustments)
        )
    else:
        action += " The daily maximum is 3 servings."

    return action


def _sleep_recommendation(sleep_quality):
    if sleep_quality <= 2:
        return None
    if sleep_quality <= 4:
        return {
            "time": "10:00 UTC",
            "category": "Sleep",
            "action": "Take a 10–15 minute nap.",
        }
    if sleep_quality <= 6:
        return {
            "time": "22:00 UTC",
            "category": "Sleep",
            "action": "Aim for 7 hours of sleep and move your sleep schedule earlier as needed.",
        }
    if sleep_quality == 7:
        return {
            "time": "22:00 UTC",
            "category": "Sleep",
            "action": "Maintain your current sleep routine.",
        }
    if sleep_quality == 8:
        return {
            "time": "21:00 UTC",
            "category": "Sleep",
            "action": "Maintain your current sleep routine.",
        }
    return {
        "time": "22:00 UTC",
        "category": "Sleep",
        "action": "Target 7–8 hours of sleep; if you currently sleep longer, reduce toward that range.",
    }


def _meal_recommendation(meals_per_day):
    if meals_per_day in (0, 1) or meals_per_day >= 4:
        action = "Target 2 meals per day."
    else:
        action = "Maintain {} meals per day.".format(meals_per_day)

    if meals_per_day in (0, 2, 3):
        action += " The caffeine change for this meal range is included in the combined caffeine target."

    return {
        "time": "10:00, 20:00 UTC",
        "category": "Meals",
        "action": action,
    }


def _build_schedule(survey):
    sleep_quality = int(survey["sleep_quality"])
    servings = int(survey["caffeine_servings_per_day"])
    meals_per_day = int(survey["meals_per_day"])

    target = _caffeine_target(servings, sleep_quality, meals_per_day)
    items = [
        {
            "time": _caffeine_times(servings, target, sleep_quality, meals_per_day),
            "category": "Caffeine",
            "action": _caffeine_action(servings, target, sleep_quality, meals_per_day),
        }
    ]

    sleep_item = _sleep_recommendation(sleep_quality)
    if sleep_item is not None:
        items.append(sleep_item)

    items.append(_meal_recommendation(meals_per_day))
    return items


@anvil.server.callable(require_user=True)
def get_personal_schedule():
    user = anvil.users.get_user()
    surveys = list(app_tables.survey_responses.search(user=user))
    if not surveys:
        return {
            "ok": False,
            "message": "No saved survey was found. Complete the survey to build your schedule.",
            "items": [],
        }

    survey = max(surveys, key=lambda row: row["submitted_at"])
    return {
        "ok": True,
        "message": "Schedule based on your latest survey. All displayed times are UTC.",
        "items": _build_schedule(survey),
    }
