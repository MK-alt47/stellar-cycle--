from ._anvil_designer import Form3Template
from anvil import *
import anvil.server


class Form3(Form3Template):
  def __init__(self, **properties):
    super().__init__(**properties)
    result = anvil.server.call("get_personal_schedule")
    self.schedule_panel.items = result["items"]
    self.status_label.text = result["message"]

  @handle("edit_survey_button", "click")
  def edit_survey_button_click(self, **event_args):
    open_form("Form2")
