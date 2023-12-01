import math
from threading import Lock


class Airport:
    def __init__(self):
        self.lock = Lock()
        self.airport_area = AirportArea(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor_1 = AirCorridor(-2000, 2000, -500, -400, 0, 2000)
        self.air_corridor_2 = AirCorridor(-2000, 2000, 400, 500, 0, 2000)
        self.airport_lanes = 2
        self.max_airplanes_number_in_the_air = 100
        self.airplanes_in_the_air_list = []
        self.crashed_airplanes = []

    def check_airplanes_number(self):
        if len(self.airplanes_in_the_air_list) > self.max_airplanes_number_in_the_air:
            message = {"Attention": "We have enough airplanes in our airspace, please fly to another airport"}
            return message

    def check_distance_between_airplanes(self):
        if len(self.airplanes_in_the_air_list) > 1:
            for i, airplane_1 in enumerate(self.airplanes_in_the_air_list):
                for j, airplane_2 in enumerate(self.airplanes_in_the_air_list):
                    if i != j:
                        distance = self.euclidean_formula(airplane_1, airplane_2)
                        if distance <= 10:
                            print(f"Collision between {airplane_1} and {airplane_2}")
                            self.crashed_airplanes.extend([airplane_1, airplane_2])
                        if distance in range(10, 1000):
                            message = {"Distance": "You`re to close to another airplane. Change your position"}
                            return message
            self.remove_crashed_airplanes_from_the_list()

    @staticmethod
    def euclidean_formula(airplane_1, airplane_2):
        distance = math.sqrt((
            pow(airplane_1.x - airplane_2.x, 2) +
            pow(airplane_1.y - airplane_2.y, 2) +
            pow(airplane_1.z - airplane_2.z, 2)
        ))
        return distance

    def remove_crashed_airplanes_from_the_list(self):
        for airplane in self.crashed_airplanes:
            self.airplanes_in_the_air_list.remove(airplane)


class AirportArea:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)


class AirCorridor:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.occupied = False
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)




