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
    fields = (
      self.sleep_hours_box,
      self.weight_kg_box,
      self.caffeine_box,
      self.height_feet_box,
      self.meals_per_day_box,
      self.sleep_quality_box,
    )
    if any(not str(field.text or "").strip() for field in fields):
      self.account_status_label.text = "Please complete every survey field."
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
