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

    def check_distance_between_airplanes(self, airplane_object, airplane_id, airplanes_list):
        if len(airplanes_list) > 1:
            airplane_x = airplane_object[airplane_id]["coordinates"][0]
            airplane_y= airplane_object[airplane_id]["coordinates"][1]
            airplane_z = airplane_object[airplane_id]["coordinates"][2]
            for other_airplane in airplanes_list:
                if other_airplane.airplane_object[other_airplane.airplane_key] != airplane_id:
                    other_airplane_x = other_airplane.airplane_object[other_airplane.airplane_key]["coordinates"][0]
                    other_airplane_y = other_airplane.airplane_object[other_airplane.airplane_key]["coordinates"][1]
                    other_airplane_z = other_airplane.airplane_object[other_airplane.airplane_key]["coordinates"][2]
                    distance = euclidean_formula(airplane_x, airplane_y, airplane_z,
                                                 other_airplane_x, other_airplane_y, other_airplane_z)
                    if 10 < distance < 100:
                        return 0        # airplane has to avoid collision
                    elif distance < 10:
                        return 1        # airplanes crashed
        return 2                        # everything`s ok


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

