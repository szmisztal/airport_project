import datetime
import random
from server.math_calculation import euclidean_formula, movement_formula


class Airplane:
    """
    Class representing an airplane in the airport simulation.

    Attributes:
    - client: Client handling the airplane's communication with the server.
    - date_of_appearance: Date and time of the airplane's appearance.
    - id: Identifier of the airplane.
    - x: X-coordinate of the airplane.
    - y: Y-coordinate of the airplane.
    - z: Z-coordinate of the airplane.
    - quarter: Quarter where the airplane is located.
    - initial_landing_point: Initial landing point of the airplane.
    - waiting_point: Waiting point of the airplane, when runaway is occupied.
    - zero_point: Airplane landing place.
    - speed: Speed of the airplane.
    - fly_to_initial_landing_point: Flag indicating whether the airplane is flying to the initial landing point.
    - fly_to_runaway: Flag indicating whether the airplane is flying to the runway.
    - fly_to_waiting_point: Flag indicating whether the airplane is flying to the waiting point.
    """

    def __init__(self, client, coordinates):
        """
        Initializes the airplane object.

        Parameters:
        - client: Client handling the airplane's communication with the server.
        - coordinates: Dictionary containing the initial coordinates of the airplane.
        """
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
        """
        Generates random initial coordinates for an airplane, ensuring that the airplane appears at the airport boundary
        with a minimum height of 2000.

        Returns:
        - coordinates_dict: Dictionary containing random initial coordinates for the airplane, including 'x', 'y', and 'z'.
        """
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
        """
        Sets the movement points of the airplane based on the provided dictionary.

        Parameters:
        - points: A dictionary containing the points of the airplane, including the quarter, initial landing point,
                  waiting point, and zero point coordinates.
        """
        self.quarter = points["body"]
        self.initial_landing_point = points["init_point_coordinates"]
        self.waiting_point = points["waiting_point_coordinates"]
        self.zero_point = points["zero_point_coordinates"]

    def fuel_consumption(self):
        """
        Checks the fuel consumption of the airplane based on the time since its appearance.

        Returns:
        - bool: False if the airplane has been running for more than 3 hours (10800 seconds), indicating it's out of fuel,
                True otherwise.
        """
        current_time = datetime.datetime.now()
        time_difference = current_time - self.date_of_appearance
        if time_difference >= datetime.timedelta(seconds = 10800):
            return False
        return True

    def fly_to_target(self, target):
        """
        Calculates the distance to the target coordinates and moves the airplane accordingly.

        Parameters:
        - target: A list containing the x, y, and z coordinates of the target.

        Returns:
        - float: The distance between the current position of the airplane and the target coordinates.
        """
        distance = euclidean_formula(self.x, self.y, self.z, target[0], target[1], target[2])
        movement_formula(self, target[0], target[1], target[2])
        return distance

    def avoid_collision(self, avoidance_distance):
        """
        Moves the airplane to avoid a collision by adjusting its coordinates.

        Parameters:
        - avoidance_distance: The distance by which the airplane should move to avoid the collision.

        Returns:
        - tuple: A tuple containing the updated x, y, and z coordinates of the airplane after avoiding the collision.
        """
        self.x += avoidance_distance
        self.y += avoidance_distance
        self.z += 10
        return self.x , self.y, self.z

    def count_distance_and_send_airplane_coordinates(self, client_socket, target_coordinates):
        """
        Calculates the distance to the target coordinates, sends the airplane coordinates to the client socket,
        and returns the calculated distance.

        Parameters:
        - client_socket: The socket used for communication with the client.
        - target_coordinates: A list containing the x, y, and z coordinates of the target.

        Returns:
        - float: The distance between the current position of the airplane and the target coordinates.
        """
        distance = self.fly_to_target(target_coordinates)
        self.client.send_airplane_coordinates(client_socket, 1)
        return distance

    def direct_to_initial_landing_point(self, client_socket):
        """
        Directs the airplane to the initial landing point and handles the response from the server.

        Parameters:
        - client_socket: The socket used for communication with the client.
        """
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
        """
        Directs the airplane to the waiting point and updates the flags accordingly.

        Parameters:
        - client_socket: The socket used for communication with the client.
        """
        distance = self.count_distance_and_send_airplane_coordinates(client_socket, self.waiting_point)
        if distance < 100:
            self.fly_to_waiting_point = False
            self.fly_to_initial_landing_point = True

    def direct_to_runaway(self, client_socket):
        """
        Directs the airplane to the runway and handles the landing procedure.

        Parameters:
        - client_socket: The socket used for communication with the client.
        """
        distance = self.count_distance_and_send_airplane_coordinates(client_socket, self.zero_point)
        if distance < 50:
            self.client.send_message_to_server(client_socket, self.client.communication_utils.successfully_landing_message())
            self.client.is_running = False

    def airplane_movement_manager(self, client_socket):
        """
        Manages the movement of the airplane based on its current state and fuel availability.

        Parameters:
        - client_socket: The socket used for communication with the client.
        """
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
        """
        Parses the airplane object attributes into a JSON format.

        Returns:
        - dict: A dictionary containing the airplane attributes in JSON format.
        """
        return {
            f"Airplane_{self.id}": {
                "coordinates": [self.x, self.y, self.z],
                "quarter": self.quarter,
                "initial_landing_point": self.initial_landing_point,
                "waiting_point": self.waiting_point,
                "zero_point": self.zero_point,
            }
        }

