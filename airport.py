import itertools
from math_patterns import euclidean_formula


class Airport:
    def __init__(self):
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.initial_landing_point_NW = CustomPoint(-2500, 450, 2000)
        self.initial_landing_point_NE = CustomPoint(2500, 450, 2000)
        self.initial_landing_point_SW = CustomPoint(-2500, -450, 2000)
        self.initial_landing_point_SE = CustomPoint(2500, -450, 2000)
        self.waiting_point_for_landing_NW = CustomPoint(-3250, 800, 2350)
        self.waiting_point_for_landing_NE = CustomPoint(3250, 800, 2350)
        self.waiting_point_for_landing_SW = CustomPoint(-3250, -800, 2350)
        self.waiting_point_for_landing_SE = CustomPoint(3250, -800, 2350)
        self.air_corridor_N = AirCorridor("N")
        self.air_corridor_S = AirCorridor("S")
        self.zero_point_N = CustomPoint(0, 450 ,0)
        self.zero_point_S = CustomPoint(0, -450, 0)

    @staticmethod
    def establish_airplane_quarter(coordinates):
        if coordinates["x"] in range(-5000, 0) and coordinates["y"] in range(0, 5001):
             return "NW"
        elif coordinates["x"] in range(0, 5001) and coordinates["y"] in range(0, 5001):
            return "NE"
        elif coordinates["x"] in range(-5000, 0) and coordinates["y"] in range(-5000, 0):
            return "SW"
        elif coordinates["x"] in range(0, 5001) and coordinates["y"] in range(-5000, 0):
            return "SE"

    def check_distance_between_airplanes(self):
        if len(self.airplanes_in_the_air_list) > 1:
            all_airplanes_combinations = list(itertools.combinations(self.airplanes_in_the_air_list, 2))
            for airplane_combination in all_airplanes_combinations:
                distance = euclidean_formula(airplane_combination[0], airplane_combination[1])
                if 11 < distance < 100:
                    self.avoid_collision(airplane_combination[0])
                elif distance <= 10:
                    self.crashed_airplanes.append(airplane_combination[0])
                    self.crashed_airplanes.append(airplane_combination[1])
            self.remove_airplane_from_the_airplanes_in_the_air_list(self.crashed_airplanes)

    def avoid_collision(self, airplane, avoidance_distance = 50):
        airplane.x += avoidance_distance
        airplane.y += avoidance_distance
        airplane.z += 10

        # airplanes_combinations = list(itertools.product(airplane_1, self.airplanes_in_the_air_list))
        # for airplane_combination in airplanes_combinations:
        #     distance = euclidean_formula(airplane_combination[0].z + avoidance_distance, airplane_combination[1])
        #     if airplane_combination[0] != airplane_combination[1] and distance > 150:
        #         airplane_combination[0].z += avoidance_distance
        #         return airplane_combination[0]


class AirCorridor:
    def __init__(self, direction):
        self.direction = direction
        self.occupied = False


class CustomSector:
    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2


class CustomPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def point_coordinates(self):
        return [self.x, self.y, self.z]

