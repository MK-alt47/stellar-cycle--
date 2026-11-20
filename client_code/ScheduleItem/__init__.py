from ._anvil_designer import ScheduleItemTemplate


class ScheduleItem(ScheduleItemTemplate):
  def __init__(self, **properties):
    super().__init__(**properties)
