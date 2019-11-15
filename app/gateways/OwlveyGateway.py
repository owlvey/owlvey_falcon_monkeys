import datetime

import requests


class OwlveyGateway:

    def __init__(self):
        # self.host = "http://localhost:5001"
        self.host = "http://localhost:50001"
        # self.identity = "http://localhost:5000"
        self.identity = "http://localhost:50000"
        self.token = None
        self.token_on = None
        self.client_id = "CF4A9ED44148438A99919FF285D8B48D"
        self.client_secret = "0da45603-282a-4fa6-a20b-2d4c3f2a2127"

    @staticmethod
    def __validate_status_code(response, url=""):
        if response.status_code > 299:
            raise ValueError(url + "\n" + response.status_code + "\n" + response.text)

    def generate_token(self):
        payload = {
            "grant_type": "client_credentials",
            "scope": "api",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(self.identity + "/connect/token",
                                 data=payload)
        OwlveyGateway.__validate_status_code(response)
        self.token_on = datetime.datetime.now()
        self.token = response.json()

    def __build_authorization_header(self):
        if self.token:
            expires_in = self.token["expires_in"]
            if (self.token_on + datetime.timedelta(seconds=expires_in + 30)) > datetime.datetime.now():
                self.generate_token()
        else:
            self.generate_token()

        return {
            "Authorization": "Bearer " + self.token["access_token"]
        }

    def __internal_get(self, url):
        response = requests.get(url,
                                headers=self.__build_authorization_header(),
                                verify=False)
        OwlveyGateway.__validate_status_code(response)
        return response.json()

    def __internal_put(self, url, payload):
        response = requests.put(url, json=payload,
                                headers=self.__build_authorization_header(),
                                verify=False)
        OwlveyGateway.__validate_status_code(response)

    def __internal_post(self, url, payload):
        response = requests.post(url, json=payload,
                                 headers=self.__build_authorization_header(),
                                 verify=False)
        OwlveyGateway.__validate_status_code(response, url)
        return response.json()

    def get_customers(self):
        return self.__internal_get(self.host + "/customers")

    def get_products(self, customer_id):
        return self.__internal_get(self.host + '/products?customerId={}'.format(customer_id))

    def get_services(self, product_id):
        return self.__internal_get(self.host + '/services?productId={}'.format(product_id))

    def get_syncs(self, product_id):
        return self.__internal_get(self.host + "/products/{}/sync".format(product_id))

    def post_sync(self, product_id, name):
        return self.__internal_post(self.host + "/products/{}/sync/{}".format(product_id, name), {})

    def put_last_anchor(self, product_id, name, target):
        self.__internal_put(self.host + "/products/{}/sync/{}".format(product_id, name),
                            {"target": target.isoformat()})

    def get_features(self, product_id):
        return self.__internal_get(self.host + "/features?productId={}".format(product_id))

    def create_customer(self, name):
        return self.__internal_post(self.host + "/customers", {"name": name})

    def create_product(self, customer_id, name):
        return self.__internal_post(self.host + "/products", {"customerId": customer_id, "name": name})

    def create_service(self, product_id, name, slo):
        service = self.__internal_post(self.host + "/services", {"productId": product_id, "name": name})
        service_id = service["id"]
        service["slo"] = slo
        self.__internal_put(self.host + "/services/" + str(service_id), service)
        return service

    def create_feature(self, product_id, name):
        return self.__internal_post(self.host + "/features", {"productId": product_id, "name": name})

    def create_service_map(self, service_id, feature_id):
        return self.__internal_put(self.host + "/services/{}/features/{}".format(service_id, feature_id), {})

    def create_incident(self, product_id, key, title, resolution_on: datetime, ttd, tte, ttf, url):
        response = requests.post(self.host + "/incidents", json={"productId": product_id,
                                                                 "key": key,
                                                                 "title": title
                                                                 },
                                 verify=False)
        OwlveyGateway.__validate_status_code(response)
        incident_id = response.json()["id"]
        response = requests.put(self.host + "/incidents/{}".format(incident_id),
                                json={"title": title, "ttd": ttd, "tte": tte, "ttf": ttf, "url": url,
                                      "affected": 1,
                                      "end": resolution_on.isoformat()},
                                verify=False)
        OwlveyGateway.__validate_status_code(response)

        return response.json()

    def assign_incident_feature(self, incident_id, feature_id):
        response = requests.put(self.host + "/incidents/{}/features/{}".format(incident_id, feature_id),
                                verify=False)
        OwlveyGateway.__validate_status_code(response)

    def create_source(self, product_id, name):
        return self.__internal_post(self.host + "/sources", {"productId": product_id, "name": name})

    def create_sli(self, feature_id, source_id):
        self.__internal_put(self.host + "/features/{}/indicators/{}".format(feature_id, source_id), {})

    def search_feature(self, product_id, name):
        return self.__internal_get(self.host + "/features/search?productId={}&name={}".format(product_id, name))

    def create_source_item(self, source_id, start, end, total, good):
        try:
            return self.__internal_post(self.host + "/sourceItems",
                                        {
                                            "sourceId": source_id,
                                            "start": start.isoformat(),
                                            "end": end.isoformat(),
                                            "total": int(total),
                                            "good": int(good)
                                         })

        except ValueError as e:
            print("problem {} | {} |".format(start.isoformat, good, total))

        return {}












