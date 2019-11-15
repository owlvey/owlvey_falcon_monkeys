import unittest

from app.components.GarfieldComponent import GarfieldComponent


class TestGarfieldComponent(unittest.TestCase):

    def test_fill_customers_empty(self):
        garfield = GarfieldComponent()
        garfield.fill_empty_customers()


if __name__ == "__main__":
    unittest.main()


