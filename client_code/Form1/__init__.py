from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class Form1(Form1Template):
  def __init__(self, **properties):
    super().__init__(**properties)

  @handle("", "show")
  def form_show(self, **event_args):
    """This method is called when the form is shown on the page"""
    pass  # Write Code Here
