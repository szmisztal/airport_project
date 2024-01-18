import datetime
import random


class Airplane:
    def __init__(self, coordinates):
        self.date_of_appearance = datetime.datetime.now()
        self.id = None
        self.x = coordinates["x"]
        self.y = coordinates["y"]
        self.z = coordinates["z"]
        self.quarter = None
        self.initial_landing_point = None
        self.waiting_point = None
        self.zero_point = None
        self.speed = 100
        self.move_to_initial_landing_point = True
        self.move_to_waiting_sector = False
        self.move_to_runaway = False

    @staticmethod
    def establish_init_airplane_coordinates():
        height = random.randint(2000, 5000)
        random_int = random.randint(-5000, 5000)
        constant = 5000
        neg_constant = -5000
        possible_coordinates = [
            [random_int, constant, height],
            [random_int, neg_constant, height],
            [constant, random_int, height],
            [neg_constant, random_int, height]
        ]
        choose_option = random.choice(possible_coordinates)
        coordinates_dict = {
            "x": choose_option[0],
            "y": choose_option[1],
            "z": choose_option[2]
        }
        return coordinates_dict

    def set_points(self, points):
        self.quarter = points.get("quarter")
        self.initial_landing_point = points.get("initial_landing_point")
        self.waiting_point = points.get("waiting_point")
        self.zero_point = points.get("zero_point")

    def fuel_consumption(self):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.date_of_appearance
        if time_difference >= datetime.timedelta(seconds=10800):
            return time_difference
        return None

    def parse_airplane_obj_to_json(self):
        return {
            f"Airplane_{self.id}": {
                "coordinates": [self.x, self.y, self.z],
                "quarter": self.quarter,
                "initial_landing_point": self.initial_landing_point,
                "waiting_point": self.waiting_point,
                "zero_point": self.zero_point,
                "move_to_initial_landing_point": self.move_to_initial_landing_point,
                "move_to_waiting_point": self.move_to_waiting_sector,
                "move_to_runaway": self.move_to_runaway
            }
        }


