
#  this component will fill information in empty resources
from datetime import datetime
from app.core.AvailabilityUtil import AvailabilityUtil
from app.gateways.OwlveyGateway import OwlveyGateway
import calendar

class GarfieldComponent:

    def __init__(self):
        self.owlvey = OwlveyGateway()

    def fill_empty_customers(self):
        customers = self.owlvey.get_customers()
        for customer in customers:
            products = self.owlvey.get_products(customer["id"])
            for product in products:
                services = self.owlvey.get_services(product["id"])
                features = self.owlvey.get_features(product["id"])
                if len(services) == 0 and len(features) == 0:
                    self.fill_empty_product(product["id"])

    def fill_empty_products(self):
        pass

    def fill_empty_product(self, product_id):
        home_feature = self.__fill_feature(product_id, "home",
                                      [("/home/images", 0.99),
                                       ("/home/messages", 0.98),
                                       ("/home/alerts", 0.97)])

        notifications_feature = self.__fill_feature(product_id, "notifications",
                                      [("/notifications/premium", 0.97),
                                       ("/notifications/alerts", 0.98),
                                       ("/notifications/opportunities", 0.99)])

        service = self.owlvey.create_service(product_id, "welcome", 0.99)

        self.owlvey.create_service_map(service["id"], home_feature["id"])
        self.owlvey.create_service_map(service["id"], notifications_feature["id"])

        dashboard_feature = self.__fill_feature(product_id, "dashboard",
                                                [("/dashboard/messages", 0.99),
                                                 ("/dashboard/favorites", 0.98),
                                                 ("/dashboard/status", 0.97)])

        login_feature = self.__fill_feature(product_id, "login",
                                      [("/login/first_step", 0.99),
                                       ("/login/second_step", 0.98),
                                       ("/login/confirm", 0.97)])
        login_service = self.owlvey.create_service(product_id, "login", 0.99)

        self.owlvey.create_service_map(login_service["id"], login_feature["id"])
        self.owlvey.create_service_map(login_service["id"], dashboard_feature["id"])

        on_boarding_feature = self.__fill_feature(product_id, "on boarding",
                                      [("/onboarding/sing", 0.99),
                                       ("/onboarding/confirm", 0.98),
                                       ("/onboarding/email", 0.97)])
        on_boarding_service = self.owlvey.create_service(product_id, "on boarding", 0.99)

        self.owlvey.create_service_map(on_boarding_service["id"], on_boarding_feature["id"])
        self.owlvey.create_service_map(on_boarding_service["id"], dashboard_feature["id"])

        accounts_feature = self.__fill_feature(product_id, "accounts",
                                      [("/accounts/search", 0.99),
                                       ("/accounts/get", 0.98)])

        payments_feature = self.__fill_feature(product_id, "payments",
                                      [("/payments/sing", 0.99),
                                       ("/payments/confirm", 0.98),
                                       ("/payments/email", 0.97)])

        payment_service = self.owlvey.create_service(product_id, "payments", 0.90)

        self.owlvey.create_service_map(payment_service["id"], login_feature["id"])
        self.owlvey.create_service_map(payment_service["id"], dashboard_feature["id"])
        self.owlvey.create_service_map(payment_service["id"], accounts_feature["id"])
        self.owlvey.create_service_map(payment_service["id"], payments_feature["id"])

        transfers_feature = self.__fill_feature(product_id, "transfers",
                                                [("/transfers/sing", 0.99),
                                                 ("/transfers/confirm", 0.98),
                                                 ("/transfers/email", 0.97)])

        transfers_service = self.owlvey.create_service(product_id, "payments", 0.90)
        self.owlvey.create_service_map(transfers_service["id"], login_feature["id"])
        self.owlvey.create_service_map(transfers_service["id"], dashboard_feature["id"])
        self.owlvey.create_service_map(transfers_service["id"], accounts_feature["id"])
        self.owlvey.create_service_map(transfers_service["id"], transfers_feature["id"])

        profile_feature = self.__fill_feature(product_id, "profile",
                                                [("/profile/get", 0.99),
                                                 ("/profile/detail", 0.98),
                                                 ("/profile/email", 0.97)])

        profile_service = self.owlvey.create_service(product_id, "profile", 0.80)
        self.owlvey.create_service_map(profile_service["id"], login_feature["id"])
        self.owlvey.create_service_map(profile_service["id"], dashboard_feature["id"])
        self.owlvey.create_service_map(profile_service["id"], accounts_feature["id"])
        self.owlvey.create_service_map(profile_service["id"], profile_feature["id"])


    def __fill_feature(self, product_id, name, sources):

        feature = self.owlvey.create_feature(product_id, name)
        for item in sources:
            source = self.__create_source_daily(product_id, item[0], item[1])
            self.owlvey.create_sli(feature["id"], source["id"])
        return feature

    def __create_source(self, product_id, name, slo):
        source = self.owlvey.create_source(product_id, name)
        year = datetime.now().year
        for item in range(1, 13):
            s, e = calendar.monthrange(datetime.now().year, item)
            start = datetime(year, item, 1)
            end = datetime(year, item, e)
            good, total = AvailabilityUtil.generate_data(slo)
            self.owlvey.create_source_item(source["id"], start, end, total, good)

        return source

    def __create_source_daily(self, product_id, name, slo):
        source = self.owlvey.create_source(product_id, name)
        year = datetime.now().year
        month = datetime.now().month
        months = range(month - 3, month + 1) if month > 4 else range(1, month + 1)
        for item in months:
            s, e = calendar.monthrange(datetime.now().year, item)
            for day in range(1, e + 1):
                start = datetime(year, item, day)
                good, total = AvailabilityUtil.generate_data(slo)
                self.owlvey.create_source_item(source["id"], start, start, total, good)
        return source








