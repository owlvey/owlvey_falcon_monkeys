from random import random
from random import gauss


class AvailabilityUtil:

    @staticmethod
    def generate_data(slo):

        test = gauss(0.1, 0.1)

        if test > 0:
            sd = (1 - slo) / 3
        else:
            sd = (1 - slo)

        value = gauss(slo - sd, sd)
        if value > 1:
            return 1000, 1000
        if value < 0:
            return 0, 1000
        return round(value * 1000, 0), 1000
