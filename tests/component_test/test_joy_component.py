import unittest

from app.components.JoyComponent import JoyComponent
from app.core.CalendarUtils import CalendarUtils


class TestJoyComponent(unittest.TestCase):

    def test_joy_component_setup(self):
        self.joy_component = JoyComponent()
        self.joy_component.setup()

    def test_joy_anchors_reset(self):
        self.joy_component = JoyComponent()
        self.joy_component.setup()
        self.joy_component.reset_sync()

    def test_joy_load_services_metadata(self):
        self.joy_component = JoyComponent()
        self.joy_component.setup()
        self.joy_component.load_service_metadata()

    def test_joy_sync(self):
        self.joy_component = JoyComponent("DFP500")
        self.joy_component.sync_joy(False)

    def test_joy_sync_400_500(self):
        self.joy_component = JoyComponent()
        self.joy_component.sync_joy(True)
