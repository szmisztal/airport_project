import datetime
import random


class Airplane:
    def __init__(self, coordinates):
        self.date_of_appearance = datetime.datetime.now()
        self.id = None
        self.x = coordinates["x"]
        self.y = coordinates["y"]
        self.z = coordinates["z"]
        self.quarter = self.establish_airplane_quarter()
        self.initial_landing_point = None
        self.waiting_sector = None
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

    def establish_airplane_id(self, airplanes_in_db_number):
        airplane_id = airplanes_in_db_number + 1
        self.id = airplane_id
        return self.id

    def establish_airplane_quarter(self):
        if self.x in range(-5000, 0) and self.y in range(0, 5001):
             return "NW"
        elif self.x in range(0, 5001) and self.y in range(0, 5001):
            return "NE"
        elif self.x in range(-5000, 0) and self.y in range(-5000, 0):
            return "SW"
        elif self.x in range(0, 5001) and self.y in range(-5000, 0):
            return "SE"

    def fuel_consumption(self):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.date_of_appearance
        if time_difference >= datetime.timedelta(seconds = 10800):
            return False
        return True

    def __str__(self):
        return {f'Airplane_{self.id}': [self.x, self.y, self.z]}
