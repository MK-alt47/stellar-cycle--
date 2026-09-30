from ._anvil_designer import Form1Template
from anvil import *


class Form1(Form1Template):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("", "show")
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    pass  # Write Code Here
