from math_patterns import euclidean_formula, simulating_airplane_movement, simulating_landing


class Airport:
    def __init__(self):
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.air_corridor_N = CustomSector(-2000, 2000, 400, 500, 0, 2000)
        self.air_corridor_S = CustomSector(-2000, 2000, -500, -400, 0, 2000)
        self.starting_landing_point_NW = CustomPoint(-2500, 450, 2000)
        self.starting_landing_point_NE = CustomPoint(2500, 450, 2000)
        self.starting_landing_point_SW = CustomPoint(-2500, -450, 2000)
        self.starting_landing_point_SE = CustomPoint(2500, -450, 2000)
        self.zero_point = CustomPoint(0, 0 ,0)
        self.max_airplanes_number_in_the_air = 100
        self.airplanes_in_the_air_list = []
        self.crashed_airplanes = []
        self.airplanes_with_successfully_landing = []

    def check_airplanes_number(self):
        if len(self.airplanes_in_the_air_list) > self.max_airplanes_number_in_the_air:
            message = {"Attention": "We have enough airplanes in our airspace, please fly to another airport"}
            return message

    def check_distance_between_airplanes(self):
        if len(self.airplanes_in_the_air_list) > 1:
            for i, airplane_1 in enumerate(self.airplanes_in_the_air_list):
                for j, airplane_2 in enumerate(self.airplanes_in_the_air_list):
                    if i != j:
                        distance = euclidean_formula(airplane_1, airplane_2)
                        if 11 < distance < 100:
                            pass
                        elif distance <= 10:
                            self.crashed_airplanes.extend([airplane_1, airplane_2])
            self.remove_airplane_from_the_list(self.crashed_airplanes)

    def remove_airplane_from_the_list(self, target_group):
        for airplane in target_group:
            if airplane in self.airplanes_in_the_air_list:
                self.airplanes_in_the_air_list.remove(airplane)

    def avoid_collision(self, airplane):
        turn_x_right = airplane.x + 100
        turn_x_left = airplane.x - 100
        turn_y_up = airplane.y + 100
        turn_y_down = airplane.y - 100
        turn_z_higher = airplane.z + 50
        turn_z_lower = airplane.z - 50
        options = [turn_x_right, turn_x_left, turn_y_up, turn_y_down, turn_z_higher, turn_z_lower]

    def airport_manager(self):
        pass


class CustomSector:
    def __init__(self, x1 , x2, y1, y2, z1, z2):
        self.length = (x1, x2)
        self.width = (y1, y2)
        self.height = (z1, z2)

class CustomPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z




