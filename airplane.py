import datetime
import random
from math_patterns import euclidean_formula, movement_formula


class Airplane:
    def __init__(self, client, coordinates):
        self.client = client
        self.date_of_appearance = datetime.datetime.now()
        self.id = None
        self.x = coordinates["x"]
        self.y = coordinates["y"]
        self.z = coordinates["z"]
        self.quarter = None
        self.initial_landing_point = None
        self.waiting_point = None
        self.zero_point = None
        self.speed = 100
        self.fly_to_initial_landing_point = False
        self.fly_to_runaway = False
        self.fly_to_waiting_point = False

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

    def set_points(self, points):
        self.quarter = points["body"]
        self.initial_landing_point = points.get("init_point_coordinates")
        self.waiting_point = points.get("waiting_point_coordinates")
        self.zero_point = points.get("zero_point_coordinates")

    def fuel_consumption(self):
        current_time = datetime.datetime.now()
        time_difference = current_time - self.date_of_appearance
        if time_difference >= datetime.timedelta(seconds = 10800):
            return False
        return True

    def fly_to_target(self, target):
        distance = euclidean_formula(self.x, self.y, self.z, target[0], target[1], target[2])
        movement_formula(self, target[0], target[1], target[2])
        return distance

    def avoid_collision(self, avoidance_distance):
        self.x += avoidance_distance
        self.y += avoidance_distance
        self.z += 10
        return self.x , self.y, self.z

    def count_distance_and_send_airplane_coordinates(self, client_socket, target_coordinates):
        distance = self.fly_to_target(target_coordinates)
        self.client.send_airplane_coordinates(client_socket)
        return distance

    def direct_to_initial_landing_point(self, client_socket):
        distance = self.count_distance_and_send_airplane_coordinates(client_socket, self.initial_landing_point)
        if distance < 100:
            self.client.send_message_to_server(client_socket, self.client.communication_utils.reaching_the_target_message("Initial landing point"))
            order_from_server = self.client.read_message_from_server(client_socket)
            self.fly_to_initial_landing_point = False
            if "Waiting point" in order_from_server["body"]:
                self.fly_to_waiting_point = True
            elif "Zero point" in order_from_server["body"]:
                self.fly_to_runaway = True
                self.speed = 75

    def direct_to_waiting_point(self, client_socket):
        distance = self.count_distance_and_send_airplane_coordinates(client_socket, self.waiting_point)
        if distance < 100:
            self.fly_to_waiting_point = False
            self.fly_to_initial_landing_point = True

    def direct_to_runaway(self, client_socket):
        distance = self.count_distance_and_send_airplane_coordinates(client_socket, self.zero_point)
        if distance < 50:
            self.client.send_message_to_server(client_socket, self.client.communication_utils.successfully_landing_message())
            self.client.is_running = False

    def airplane_movement_manager(self, client_socket):
        fuel = self.fuel_consumption()
        if fuel:
            if self.fly_to_initial_landing_point:
                self.direct_to_initial_landing_point(client_socket)
            elif self.fly_to_waiting_point:
                self.direct_to_waiting_point(client_socket)
            elif self.fly_to_runaway:
                self.direct_to_runaway(client_socket)
        else:
            self.client.send_message_to_server(client_socket, self.client.communication_utils.out_of_fuel_message())
            self.client.stop(client_socket)

    def parse_airplane_obj_to_json(self):
        return {
            f"Airplane_{self.id}": {
                "coordinates": [self.x, self.y, self.z],
                "quarter": self.quarter,
                "initial_landing_point": self.initial_landing_point,
                "waiting_point": self.waiting_point,
                "zero_point": self.zero_point,
            }
        }

