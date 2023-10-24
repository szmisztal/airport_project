import random
from threading import Lock


class Airport:
    def __init__(self):
        self.lock = Lock()
        self.max_numbers_of_airplanes = 100
        self.airplanes_in_air_list = []
        self.airport_area = AirportArea(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor = AirCorridor(-3500, 3500, -250, 250, 0 , 2000)
        self.airport_lane_1 = AirportLane(-2500, 2500, 100, 150)
        self.airport_lane_2 = AirportLane(-2500, 2500, -100, -150)

    def establish_init_airplane_co_ordinates(self):
        height = random.randint(2000, 5000)
        random_int = random.randint(-5000, 5000)
        constant = 5000
        neg_constant = -5000
        possible_co_ordinates = [
            [random_int, constant, height],
            [random_int, neg_constant, height],
            [constant, random_int, height],
            [neg_constant, random_int, height]
        ]
        choose_option = random.choice(possible_co_ordinates)
        co_ordinates_dict = {
            "x": choose_option[0],
            "y": choose_option[1],
            "z": choose_option[2]
        }
        return co_ordinates_dict

class AirportLane:
    def __init__(self, x1, x2, y1, y2):
        self.occupied = False
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = 0


class AirportArea:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)


class AirCorridor:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)




