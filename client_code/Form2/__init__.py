from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.users


class Form2(Form2Template):
  def __init__(self, **properties):
    super().__init__(**properties)
    self._update_account_status()

  def _update_account_status(self):
    user = anvil.users.get_user()
    if user is None:
      self.account_status_label.text = "Sign in or create an account before saving your survey."
      self.account_button.text = "Log in or sign up"
    else:
      self.account_status_label.text = "Signed in as {}".format(user["email"])
      self.account_button.text = "Switch account"

  @handle("account_button", "click")
  def account_button_click(self, **event_args):
    user_form_result = anvil.users.login_with_form(show_signup_option=True, allow_cancel=True)
    self._update_account_status()
    if anvil.users.get_user() is None and user_form_result is not None:
      self.account_status_label.text = "Account created. Confirm your email, then log in to submit your survey."

  @handle("submit_button", "click")
  def submit_button_click(self, **event_args):
    validation_message = self._validate_survey_values()
    if validation_message:
      self.account_status_label.text = validation_message
      return

    if anvil.users.get_user() is None:
      self.account_status_label.text = "Log in or sign up before submitting your answers."
      return

    self.submit_button.enabled = False
    try:
      result = anvil.server.call(
        "save_survey",
        self.sleep_hours_box.text,
        self.weight_kg_box.text,
        self.caffeine_box.text,
        self.height_feet_box.text,
        self.meals_per_day_box.text,
        self.sleep_quality_box.text,
      )
    finally:
      self.submit_button.enabled = True

    if not result["ok"]:
      self.account_status_label.text = result["message"]
      return

    self.account_status_label.text = "Your survey response has been saved."

  def _validate_survey_values(self):
    limits = (
      ("Hours of sleep", self.sleep_hours_box.text, 0, 24, False),
      ("Weight in kilograms", self.weight_kg_box.text, 1, 500, False),
      ("Caffeine in milligrams per day", self.caffeine_box.text, 0, 2000, False),
      ("Height in feet", self.height_feet_box.text, 1, 8, False),
      ("Meals per day", self.meals_per_day_box.text, 0, 20, True),
      ("Sleep quality", self.sleep_quality_box.text, 1, 10, True),
    )

    if any(value is None or not str(value).strip() for _, value, _, _, _ in limits):
      return "Enter a number in every field, within its displayed range."

    for label, value, minimum, maximum, whole_number in limits:
      try:
        number = float(value)
      except (TypeError, ValueError):
        return "{} must be a number.".format(label)
      if not minimum <= number <= maximum:
        return "{} must be between {} and {}.".format(label, minimum, maximum)
      if whole_number and number % 1 != 0:
        return "{} must be a whole number.".format(label)

    return None
