import datetime
import random


class Airplane:
    def __init__(self, x, y, z):
        self.date_of_appearance = datetime.datetime.now()
        self.id = None
        self.x = x
        self.y = y
        self.z = z
        self.coordinates = (self.x, self.y, self.z)
        self.quarter = self.establish_airplane_quarter()
        self.initial_landing_point = None
        self.speed = 100

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

    def establish_airplane_id(self, airplanes_list):
        airplane_id = airplanes_list + 1
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
            return True
        return False

    def __str__(self):
        return f"AirplaneID: '{self.id}'"

    def __repr__(self):
        return str(self)

