import itertools
from math_patterns import euclidean_formula, movement_formula


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

    def simulate_airplanes_movement(self, airplane):
        # self.check_airplanes_fuel_reserves(airplane)
        self.check_distance_between_airplanes()
        if airplane.move_to_initial_landing_point:
            distance = euclidean_formula(airplane, airplane.initial_landing_point)
            if distance > 250:
                movement_formula(airplane, airplane.initial_landing_point.x, airplane.initial_landing_point.y, airplane.initial_landing_point.z)
            elif distance <= 250:
                airplane.move_to_initial_landing_point = False
                if airplane.quarter in ["NW", "NE"]:
                    air_corridor = self.air_corridor_N
                elif airplane.quarter in ["SW", "SE"]:
                    air_corridor = self.air_corridor_S
                if air_corridor.occupied == True:
                    airplane.move_to_waiting_sector = True
                else:
                    airplane.move_to_runaway = True
        elif airplane.move_to_runaway:
            distance = euclidean_formula(airplane, airplane.zero_point)
            if distance <= 50:
                if airplane.quarter in ["NW", "NE"]:
                    self.air_corridor_N.occupied = True
                elif airplane.quarter in ["SW", "SE"]:
                    self.air_corridor_S.occupied = True
                self.direct_airplane_to_runaway(airplane, distance)
        elif airplane.move_to_waiting_sector:
            distance = euclidean_formula(airplane, airplane.waiting_point)
            if distance <= 100:
                if airplane.quarter in ["NW", "NE"]:
                    air_corridor = self.air_corridor_N
                elif airplane.quarter in ["SW", "SE"]:
                    air_corridor = self.air_corridor_S
                self.direct_airplane_to_waiting_sector(airplane, distance, air_corridor)

    def direct_airplane_to_runaway(self, airplane, distance):
        if distance > 50:
            movement_formula(airplane, airplane.zero_point)
        elif 0 <= airplane.z <= 50 and distance <= 50:
            self.airplanes_with_successfully_landing.append(airplane)
        elif airplane.z < 0:
            self.crashed_airplanes.append(airplane)
        self.remove_airplane_from_the_airplanes_in_the_air_list(self.airplanes_with_successfully_landing)
        self.remove_airplane_from_the_airplanes_in_the_air_list(self.crashed_airplanes)

    def direct_airplane_to_waiting_sector(self, airplane, distance, air_corridor):
        if distance > 100:
            movement_formula(airplane, airplane.waiting_point)
        if 0 <= distance <= 100 and air_corridor.occupied == False:
            airplane.move_to_waiting_sector = False
            airplane.move_to_initial_landing_point = True
        else:
            pass

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

    def avoid_collision(self, airplane_1, avoidance_distance = 50):
        airplane_1.x += avoidance_distance
        airplane_1.y += avoidance_distance
        airplane_1.z += 10

        # airplanes_combinations = list(itertools.product(airplane_1, self.airplanes_in_the_air_list))
        # for airplane_combination in airplanes_combinations:
        #     distance = euclidean_formula(airplane_combination[0].z + avoidance_distance, airplane_combination[1])
        #     if airplane_combination[0] != airplane_combination[1] and distance > 150:
        #         airplane_combination[0].z += avoidance_distance
        #         return airplane_combination[0]

    def remove_airplane_from_the_airplanes_in_the_air_list(self, target_group):
        for airplane in target_group:
            if airplane in self.airplanes_in_the_air_list:
                self.airplanes_in_the_air_list.remove(airplane)

    def check_airplanes_fuel_reserves(self, airplane):
        fuel_reserve = airplane.fuel_consumption()
        if fuel_reserve == False:
            self.crashed_airplanes.append(airplane)
            self.remove_airplane_from_the_airplanes_in_the_air_list(self.crashed_airplanes)

    def airport_manager(self, clients_list):
        for airplane in clients_list:
            self.simulate_airplanes_movement(airplane)


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

