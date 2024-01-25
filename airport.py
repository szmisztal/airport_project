import matplotlib.pyplot as plt
from math_patterns import euclidean_formula


class Airport:
    def __init__(self):
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.initial_landing_point_NW = CustomPoint(-2500, 450, 2000)
        self.initial_landing_point_NE = CustomPoint(2500, 450, 2000)
        self.initial_landing_point_SW = CustomPoint(-2500, -450, 2000)
        self.initial_landing_point_SE = CustomPoint(2500, -450, 2000)
        self.waiting_point_for_landing_NW = CustomPoint(-3500, 1000, 2350)
        self.waiting_point_for_landing_NE = CustomPoint(3500, 1000, 2350)
        self.waiting_point_for_landing_SW = CustomPoint(-3500, -1000, 2350)
        self.waiting_point_for_landing_SE = CustomPoint(3500, -1000, 2350)
        self.air_corridor_N = AirCorridor("N")
        self.air_corridor_S = AirCorridor("S")
        self.zero_point_N = CustomPoint(0, 450 ,0)
        self.zero_point_S = CustomPoint(0, -450, 0)
        self.radar = Radar(self)
        self.airplanes_list = {}

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
            airplane_y = airplane_object[airplane_id]["coordinates"][1]
            airplane_z = airplane_object[airplane_id]["coordinates"][2]
            for airplane_number, airplane_details in airplanes_list.items():
                if airplane_number != airplane_id:
                    other_airplane_x = airplane_details["coordinates"][0]
                    other_airplane_y = airplane_details["coordinates"][1]
                    other_airplane_z = airplane_details["coordinates"][2]
                    distance = euclidean_formula(airplane_x, airplane_y, airplane_z,
                                                 other_airplane_x, other_airplane_y, other_airplane_z)
                    if 200 < distance < 300:
                        return False        # airplane has to avoid collision
                    elif distance < 100:
                        return None        # airplanes crashed
        return True                        # everything`s ok


class Radar:
    def __init__(self, airport):
        self.airport = airport

    def get_airplanes_with_coordinates_list(self, clients_list):
        airplanes = {}
        if len(clients_list) > 0:
            for client in clients_list:
                airplane_x = client.airplane_object[client.airplane_key]["coordinates"][0]
                airplane_y = client.airplane_object[client.airplane_key]["coordinates"][1]
                airplane_z = client.airplane_object[client.airplane_key]["coordinates"][2]
                airplane = {client.airplane_key: (airplane_x, airplane_y, airplane_z)}
                airplanes.update(airplane)
        return airplanes

    def config_a_graph(self, clients_list):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection = "3d")

        ax.set_xlim([-5000, 5000])
        ax.set_ylim([-5000, 5000])
        ax.set_zlim([0, 5000])

        points = {
            "Zero Point N": self.airport.zero_point_N,
            "Zero Point S": self.airport.zero_point_S
        }

        for label, coordinates in points.items():
            x, y, z = coordinates.point_coordinates()
            ax.scatter(x, y, z, label=label)

        airplanes = self.get_airplanes_with_coordinates_list(clients_list)
        if airplanes:
            for label, coordinates in airplanes.items():
                x, y, z = coordinates
                ax.scatter(x, y, z, label = label)

        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        ax.legend(loc = "upper left", bbox_to_anchor = (0.8, 0.8))
        plt.show()

    def draw_a_graph(self, clients_list):
        self.config_a_graph(clients_list)
        plt.show()


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
        return (self.x, self.y, self.z)

