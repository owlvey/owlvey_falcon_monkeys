
import unittest

from app.gateways.OwlveyGateway import OwlveyGateway


class TestOwlveyGateway(unittest.TestCase):

    def setUp(self):
        self.owlvey = OwlveyGateway()

    def test_generate_token(self):
        self.owlvey.generate_token()
        self.assertTrue(self.owlvey.token)

    def test_open_connection(self):
        self.owlvey.generate_token()
        customers = self.owlvey.get_customers()
        self.assertTrue(customers)

    def test_get_products(self):
        self.owlvey.generate_token()
        customers = self.owlvey.get_customers()
        for customer in customers:
            products = self.owlvey.get_products(customer["id"])
            self.assertIsNotNone(products)

    def test_get_services(self):
        self.owlvey.generate_token()
        customers = self.owlvey.get_customers()
        for customer in customers:
            products = self.owlvey.get_products(customer["id"])
            for product in products:
                services = self.owlvey.get_services(product["id"])
                self.assertIsNotNone(services)








if __name__ == "__main__":
    unittest.main()








