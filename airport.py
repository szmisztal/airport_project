import itertools
from math_patterns import euclidean_formula, movement_formula
from airplane import Airplane


class Airport:
    def __init__(self):
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.initial_landing_point_NW = CustomPoint(-2500, 450, 2000)
        self.initial_landing_point_NE = CustomPoint(2500, 450, 2000)
        self.initial_landing_point_SW = CustomPoint(-2500, -450, 2000)
        self.initial_landing_point_SE = CustomPoint(2500, -450, 2000)
        self.waiting_sector_for_landing_NW = CustomSector(-3500, -3000, 700, 900, 2200, 2500)
        self.waiting_sector_for_landing_NE = CustomSector(3000, 3500, 700, 900, 2200, 2500)
        self.waiting_sector_for_landing_SW = CustomSector(-3500, -3000, -700, -900, 2200, 2500)
        self.waiting_sector_for_landing_SE = CustomSector(3000, 3500, -700, -900, 2200, 2500)
        self.air_corridor_N = CustomSector(-2000, 2000, 400, 500, 0, 2000)
        self.air_corridor_S = CustomSector(-2000, 2000, -500, -400, 0, 2000)
        self.zero_point_N = CustomPoint(0, 450 ,0)
        self.zero_point_S = CustomPoint(0, -450, 0)
        self.airplanes_in_the_air_list = []
        self.crashed_airplanes = []
        self.airplanes_with_successfully_landing = []
        self.number_of_all_planes = int()

    def create_airplane_object_and_append_it_to_list(self, initial_coordinates, number_of_airplanes_in_db):
        airplane = Airplane(initial_coordinates)
        airplane.establish_airplane_id(number_of_airplanes_in_db)
        self.establish_all_points_and_sectors_to_move_for_airplane(airplane)
        self.airplanes_in_the_air_list.append(airplane)
        self.update_number_of_planes()
        return airplane

    def update_number_of_planes(self):
        self.number_of_all_planes = (
            len(self.airplanes_in_the_air_list) +
            len(self.crashed_airplanes) +
            len(self.airplanes_with_successfully_landing)
        )
        return self.number_of_all_planes

    def establish_all_points_and_sectors_to_move_for_airplane(self, airplane):
        if airplane.quarter == "NW":
            airplane.initial_landing_point = self.initial_landing_point_NW
            airplane.waiting_sector = self.waiting_sector_for_landing_NW
            airplane.zero_point = self.zero_point_N
        elif airplane.quarter == "NE":
            airplane.initial_landing_point = self.initial_landing_point_NE
            airplane.waiting_sector = self.waiting_sector_for_landing_NE
            airplane.zero_point = self.zero_point_N
        elif airplane.quarter == "SW":
            airplane.initial_landing_point = self.initial_landing_point_SW
            airplane.waiting_sector = self.waiting_sector_for_landing_SW
            airplane.zero_point = self.zero_point_S
        elif airplane.quarter == "SE":
            airplane.initial_landing_point = self.initial_landing_point_SE
            airplane.waiting_sector = self.waiting_sector_for_landing_SE
            airplane.zero_point = self.zero_point_S

    def simulate_airplanes_movement(self, airplane):
        self.check_airplanes_fuel_reserves(airplane)
        self.check_distance_between_airplanes()
        if airplane.move_to_initial_landing_point:
            distance = euclidean_formula(airplane, airplane.initial_landing_point)
            if distance > 250:
                movement_formula(airplane, airplane.initial_landing_point)
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
            if airplane.quarter in ["NW", "NE"]:
                self.air_corridor_N.occupied = True
            elif airplane.quarter in ["SW", "SE"]:
                self.air_corridor_S.occupied = True
            self.direct_airplane_to_runaway(airplane, distance)
        elif airplane.move_to_waiting_sector:
            distance = euclidean_formula(airplane, airplane.waiting_sector)
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
            movement_formula(airplane, airplane.waiting_sector)
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

    def airport_manager(self):
        if len(self.airplanes_in_the_air_list) > 0:
            for airplane in self.airplanes_in_the_air_list:
                self.simulate_airplanes_movement(airplane)
        else:
            print("Waiting for airplanes...")


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

