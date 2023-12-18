import itertools
from math_patterns import euclidean_formula, simulating_airplane_movement
from airplane import Airplane


class Airport:
    def __init__(self):
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor_N = CustomSector(-2000, 2000, 400, 500, 0, 2000)
        self.air_corridor_S = CustomSector(-2000, 2000, -500, -400, 0, 2000)
        self.initial_landing_point_NW = CustomPoint(-2500, 450, 2000)
        self.initial_landing_point_NE = CustomPoint(2500, 450, 2000)
        self.initial_landing_point_SW = CustomPoint(-2500, -450, 2000)
        self.initial_landing_point_SE = CustomPoint(2500, -450, 2000)
        self.waiting_sector_for_landing_NW = CustomSector(-3500, -3000, 700, 900, 2200, 2500)
        self.waiting_sector_for_landing_NE = CustomSector(3000, 3500, 700, 900, 2200, 2500)
        self.waiting_sector_for_landing_SW = CustomSector(-3500, -3000, -700, -900, 2200, 2500)
        self.waiting_sector_for_landing_SE = CustomSector(3000, 3500, -700, -900, 2200, 2500)
        self.zero_point_N = CustomPoint(0, 450 ,0)
        self.zero_point_S = CustomPoint(0, -450, 0)
        self.airplanes_in_the_air_list = []
        self.crashed_airplanes = []
        self.airplanes_with_successfully_landing = []
        self.number_of_all_planes = int()

    def create_airplane_object_and_append_it_to_list(self, initial_coordinates):
        airplane = Airplane(initial_coordinates)
        airplane.establish_airplane_id(self.number_of_all_planes)
        self.airplanes_in_the_air_list.append(airplane)
        self.update_number_of_planes()
        return airplane

    def update_number_of_planes(self):
        self.number_of_all_planes = (
            len(self.airplanes_in_the_air_list) +
            len(self.crashed_airplanes) +
            len(self.airplanes_with_successfully_landing)
        )

    def direct_airplanes_to_air_corridors(self, airplane):
        if airplane.quarter == "NW":
            airplane.initial_landing_point = self.initial_landing_point_NW
            return simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "NE":
            airplane.initial_landing_point = self.initial_landing_point_NE
            return simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "SW":
            airplane.initial_landing_point = self.initial_landing_point_SW
            return simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "SE":
            airplane.initial_landing_point = self.initial_landing_point_SE
            return simulating_airplane_movement(airplane, airplane.initial_landing_point)

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
        airplanes_combinations = list(itertools.product(airplane_1, self.airplanes_in_the_air_list))
        for airplane_combination in airplanes_combinations:
            distance = euclidean_formula(airplane_combination[0].z + avoidance_distance, airplane_combination[1])
            if airplane_combination[0] != airplane_combination[1] and distance > 150:
                airplane_combination[0].z += avoidance_distance
                return airplane_combination[0]

    def directing_airplanes_to_the_runaway(self, airplane):
        distance = euclidean_formula(airplane, airplane.initial_landing_point)
        if distance < 100:
            if airplane.quarter in ["NW", "NE"] and self.air_corridor_N.occupied == True:
                if airplane.quarter == "NW":
                    simulating_airplane_movement(airplane, self.waiting_sector_for_landing_NW)
                elif airplane.quarter == "NE":
                    simulating_airplane_movement(airplane, self.waiting_sector_for_landing_NE)
            elif airplane.quarter in ["SW", "SE"] and self.air_corridor_S.occupied == True:
                if airplane.quarter == "SW":
                    simulating_airplane_movement(airplane, self.waiting_sector_for_landing_SW)
                elif airplane.quarter == "SE":
                    simulating_airplane_movement(airplane, self.waiting_sector_for_landing_SE)
            else:
                if airplane.quarter in ["NW", "NE"]:
                    self.air_corridor_N.occupied = True
                    simulating_airplane_movement(airplane, self.zero_point_N)
                    distance = euclidean_formula(airplane, self.zero_point_N)
                elif airplane.quarter in ["SW", "SE"]:
                    self.air_corridor_S.occupied = True
                    simulating_airplane_movement(airplane, self.zero_point_S)
                    distance = euclidean_formula(airplane, self.zero_point_S)
                if 0 <= airplane.z <= 50 and distance <= 50:
                    self.airplanes_with_successfully_landing.append(airplane)
                elif airplane.z < 0:
                    self.crashed_airplanes.append(airplane)
                self.remove_airplane_from_the_airplanes_in_the_air_list(self.airplanes_with_successfully_landing)
                self.remove_airplane_from_the_airplanes_in_the_air_list(self.crashed_airplanes)

    def remove_airplane_from_the_airplanes_in_the_air_list(self, target_group):
        for airplane in target_group:
            if airplane in self.airplanes_in_the_air_list:
                self.airplanes_in_the_air_list.remove(airplane)

    def check_airplanes_fuel_reserves(self, airplane):
        fuel_reserve = airplane.fuel_consumption()
        if fuel_reserve == False:
            self.crashed_airplanes.append(airplane)
            self.remove_airplane_from_the_airplanes_in_the_air_list(self.crashed_airplanes)

    def airport_manager(self):
        for airplane in self.airplanes_in_the_air_list:
            self.check_airplanes_fuel_reserves(airplane)
            self.direct_airplanes_to_air_corridors(airplane)
            self.check_distance_between_airplanes()
            self.directing_airplanes_to_the_runaway(airplane)


class CustomSector:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.occupied = False
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)
        self.x = (x1 + x2) / 2
        self.y = (y1 + y2) / 2
        self.z = (z1 + z2) / 2


class CustomPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

