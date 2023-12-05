from math_patterns import euclidean_formula, simulating_airplane_movement


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
        self.max_airplanes_number_in_the_air = 100
        self.airplanes_in_the_air_list = []
        self.crashed_airplanes = []
        self.airplanes_with_successfully_landing = []

    def check_airplanes_number(self):
        if len(self.airplanes_in_the_air_list) > self.max_airplanes_number_in_the_air:
            return False
        else:
            return True

    def establish_air_corridor_for_each_airplane(self, airplane):
        if airplane.quarter == "NW":
            airplane.initial_landing_point = self.initial_landing_point_NW
            simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "NE":
            airplane.initial_landing_point = self.initial_landing_point_NE
            simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "SW":
            airplane.initial_landing_point = self.initial_landing_point_SW
            simulating_airplane_movement(airplane, airplane.initial_landing_point)
        elif airplane.quarter == "SE":
            airplane.initial_landing_point = self.initial_landing_point_SE
            simulating_airplane_movement(airplane, airplane.initial_landing_point)

    def check_distance_between_airplanes(self):
        if len(self.airplanes_in_the_air_list) > 1:
            for i, airplane_1 in enumerate(self.airplanes_in_the_air_list):
                for j, airplane_2 in enumerate(self.airplanes_in_the_air_list):
                    if i != j:
                        distance = euclidean_formula(airplane_1, airplane_2)
                        if 11 < distance < 100:
                            self.avoid_collision(airplane_1, airplane_2)
                        elif distance <= 10:
                            self.crashed_airplanes.extend([airplane_1, airplane_2])
            self.remove_airplane_from_the_airplanes_the_air_list(self.crashed_airplanes)

    def avoid_collision(self, airplane, avoidance_distance = 50):
        for other_airplane in self.airplanes_in_the_air_list:
            if airplane != other_airplane:
                distance = euclidean_formula(airplane, other_airplane)
                if distance < avoidance_distance:
                    airplane.z += avoidance_distance
                else:
                    airplane.z -= avoidance_distance
                return airplane
        return airplane

    def directing_the_plane_to_the_runaway(self, airplane):
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
                self.remove_airplane_from_the_airplanes_the_air_list(self.airplanes_with_successfully_landing)
                self.remove_airplane_from_the_airplanes_the_air_list(self.crashed_airplanes)

    def remove_airplane_from_the_airplanes_the_air_list(self, target_group):
        for airplane in target_group:
            if airplane in self.airplanes_in_the_air_list:
                self.airplanes_in_the_air_list.remove(airplane)

    def airport_manager(self):
        for airplane in self.airplanes_in_the_air_list:
            self.establish_air_corridor_for_each_airplane(airplane)
            self.check_distance_between_airplanes()
            self.directing_the_plane_to_the_runaway(airplane)


class CustomSector:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.occupied = False
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)


class CustomPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z




