from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.users


TRAVEL_OPTIONS = [
  "1 - Never travel",
  "2 - Travel once every few years",
  "3 - Travel once or twice a year",
  "4 - Travel almost every month",
  "5 - Travel every day",
]


class Form2(Form2Template):
  def __init__(self, **properties):
    super().__init__(**properties)
    self.questions = [
      {
        "key": "height",
        "prompt": "Enter your height",
        "hint": "Use feet.inches: 5.4 means 5 feet 4 inches. Use 5.10 for 5 feet 10 inches. Range: 1.0 to 8.11.",
        "kind": "height",
      },
      {
        "key": "weight",
        "prompt": "Enter your weight",
        "hint": "Choose pounds or kilograms. Allowed: 1–500 kg, or about 2.205–1,102.311 lb. Stored weight is converted to kilograms.",
        "kind": "weight",
      },
      {
        "key": "timezone_offset",
        "prompt": "Enter your home time zone",
        "hint": "Enter a whole-hour UTC offset from -11 to +12, such as -5 or +3.",
        "kind": "integer",
        "error": "Time zone must be a whole-hour offset from -11 to +12.",
      },
      {
        "key": "bedtime_hour",
        "prompt": "What hour do you usually go to bed?",
        "hint": "Use 24-hour time: 0 for midnight, 13 for 1 PM, and 23 for 11 PM.",
        "kind": "integer",
        "error": "Bedtime must be a whole number from 0 to 23.",
      },
      {
        "key": "sleep_quality",
        "prompt": "How well do you usually sleep?",
        "hint": "1 means terribly and 10 means amazing.",
        "kind": "choice",
        "options": [str(n) for n in range(1, 11)],
        "error": "Choose a sleep rating from 1 to 10.",
      },
      {
        "key": "travel_frequency",
        "prompt": "How often do you travel outside your state or country?",
        "hint": "Choose the answer that best describes your usual travel.",
        "kind": "choice",
        "options": TRAVEL_OPTIONS,
        "error": "Choose one of the listed travel options.",
      },
      {
        "key": "caffeine_servings_per_day",
        "prompt": "How many cups of coffee or cans of energy drink do you usually have per day?",
        "hint": "Enter a whole number from 0 to 50 servings per day.",
        "kind": "integer",
        "error": "Caffeine servings must be a whole number from 0 to 50 per day.",
      },
      {
        "key": "meals_per_day",
        "prompt": "How many meals do you usually eat per day?",
        "hint": "Enter a whole number from 0 to 20.",
        "kind": "integer",
        "error": "Meals must be a whole number from 0 to 20 per day.",
      },
    ]
    self.responses = {}
    self.draft_answers = {}
    self.question_index = 0
    self._update_account_status()
    self._render_question()

  def _update_account_status(self):
    user = anvil.users.get_user()
    if user is None:
      self.account_status_label.text = "Sign in or create an account before saving your survey."
      self.account_button.text = "Log in or sign up"
    else:
      self.account_status_label.text = "Signed in as {}".format(user["email"])
      self.account_button.text = "Switch account"

  def _render_question(self):
    question = self.questions[self.question_index]
    kind = question["kind"]
    draft = self.draft_answers.get(self.question_index)

    self.progress_label.text = "Question {} of {}".format(
      self.question_index + 1, len(self.questions)
    )
    self.question_label.text = str(question["prompt"])
    self.hint_label.text = str(question["hint"])

    is_choice = kind == "choice"
    is_weight = kind == "weight"
    self.answer_dropdown.visible = is_choice
    self.weight_unit_dropdown.visible = is_weight
    self.answer_box.visible = not is_choice

    if is_choice:
      options = question["options"]
      self.answer_dropdown.items = options if isinstance(options, list) else []
      self.answer_dropdown.include_placeholder = True
      self.answer_dropdown.placeholder = "Select an answer"
      self.answer_dropdown.selected_value = draft
      self.answer_box.text = ""
    elif is_weight:
      self.answer_box.type = "number"
      self.answer_box.placeholder = "Enter your weight"
      if isinstance(draft, dict):
        self.answer_box.text = draft.get("value", "")
        self.weight_unit_dropdown.selected_value = draft.get("unit")
      else:
        self.answer_box.text = ""
        self.weight_unit_dropdown.selected_value = None
      self.weight_unit_dropdown.items = ["kg", "lb"]
      self.weight_unit_dropdown.include_placeholder = True
      self.weight_unit_dropdown.placeholder = "Choose kg or lb"
    else:
      self.answer_box.type = "text" if kind == "height" else "number"
      self.answer_box.placeholder = "Enter feet.inches" if kind == "height" else "Enter a whole number"
      self.answer_box.text = draft if isinstance(draft, str) else ""
      self.weight_unit_dropdown.selected_value = None

    self.back_button.enabled = self.question_index > 0
    self.next_button.text = (
      "Save survey response"
      if self.question_index == len(self.questions) - 1
      else "Next"
    )

  def _current_draft(self):
    kind = self.questions[self.question_index]["kind"]
    if kind == "choice":
      return self.answer_dropdown.selected_value
    if kind == "weight":
      return {
        "value": self.answer_box.text,
        "unit": self.weight_unit_dropdown.selected_value,
      }
    return self.answer_box.text

  def _validate_current_answer(self):
    question = self.questions[self.question_index]
    kind = question["kind"]
    draft = self._current_draft()

    if kind == "choice":
      options = question["options"]
      if not isinstance(options, list) or draft not in options:
        return None, question["error"]
      if question["key"] == "sleep_quality":
        return int(draft), None
      return draft, None

    if kind == "weight":
      raw_value = draft["value"]
      unit = draft["unit"]
      if not str(raw_value).strip() or unit not in ("kg", "lb"):
        return None, "Choose kg or lb and enter your weight."
      try:
        value = float(raw_value)
      except (TypeError, ValueError):
        return None, "Weight must be a number."
      kg = value if unit == "kg" else value * 0.453592
      if not 1 <= kg <= 500:
        return None, "Weight must be between 1 and 500 kg, or the equivalent in pounds."
      return {"value": value, "unit": unit}, None

    raw_value = str(draft or "").strip()
    if not raw_value:
      return None, "Answer this question before continuing."

    if kind == "height":
      parsed = self._parse_height(raw_value)
      if parsed is None:
        return None, "Enter height as feet.inches, with inches from 0 to 11 (for example, 5.4)."
      return raw_value, None

    try:
      value = int(raw_value)
    except (TypeError, ValueError):
      return None, question["error"]
    if question["key"] == "timezone_offset":
      minimum, maximum = -11, 12
    elif question["key"] == "bedtime_hour":
      minimum, maximum = 0, 23
    elif question["key"] == "caffeine_servings_per_day":
      minimum, maximum = 0, 50
    else:
      minimum, maximum = 0, 20
    if not minimum <= value <= maximum:
      return None, question["error"]
    return value, None

  @staticmethod
  def _parse_height(value):
    parts = value.strip().split(".")
    if len(parts) not in (1, 2) or not parts[0].isdigit():
      return None
    feet = int(parts[0])
    inches_text = parts[1] if len(parts) == 2 else "0"
    if not inches_text.isdigit() or len(inches_text) > 2:
      return None
    inches = int(inches_text)
    if not 1 <= feet <= 8 or not 0 <= inches <= 11:
      return None
    return feet + inches / 12.0

  @handle("account_button", "click")
  def account_button_click(self, **event_args):
    user_form_result = anvil.users.login_with_form(show_signup_option=True, allow_cancel=True)
    self._update_account_status()
    if anvil.users.get_user() is None and user_form_result is not None:
      self.account_status_label.text = "Account created. Confirm your email, then log in to submit your survey."

  @handle("back_button", "click")
  def back_button_click(self, **event_args):
    self.draft_answers[self.question_index] = self._current_draft()
    if self.question_index > 0:
      self.question_index -= 1
      self.account_status_label.text = ""
      self._render_question()

  @handle("next_button", "click")
  def next_button_click(self, **event_args):
    self.draft_answers[self.question_index] = self._current_draft()
    response, validation_message = self._validate_current_answer()
    if validation_message:
      self.account_status_label.text = validation_message
      return

    question = self.questions[self.question_index]
    self.responses[question["key"]] = response
    self.account_status_label.text = ""

    if self.question_index < len(self.questions) - 1:
      self.question_index += 1
      self._render_question()
      return

    if anvil.users.get_user() is None:
      self.account_status_label.text = "Log in or sign up before saving your answers."
      return

    self.next_button.enabled = False
    try:
      weight = self.responses["weight"]
      result = anvil.server.call(
        "save_survey",
        self.responses["height"],
        weight["value"],
        weight["unit"],
        self.responses["timezone_offset"],
        self.responses["bedtime_hour"],
        self.responses["sleep_quality"],
        self.responses["travel_frequency"],
        self.responses["caffeine_servings_per_day"],
        self.responses["meals_per_day"],
      )
    finally:
      self.next_button.enabled = True

    if not result["ok"]:
      self.account_status_label.text = result["message"]
      return

    self.account_status_label.text = "Your survey response has been saved."
