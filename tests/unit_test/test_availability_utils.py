import unittest
from datetime import datetime, date
import pytz

from app.core.AvailabilityUtil import AvailabilityUtil


class TestAvailabilityUtils(unittest.TestCase):

    def test_convert_utils(self):
        value = AvailabilityUtil.generate_data(0.99)
        print(value)

















