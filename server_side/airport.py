import matplotlib.pyplot as plt
from server_side.math_calculation import euclidean_formula


class Airport:
    """
    Represents an airport in the simulation.

    Attributes:
    - airport_area: CustomSector object representing the area of the airport.
    - initial_landing_point: Dictionary containing initial landing points for airplanes in different directions.
    - waiting_point: Dictionary containing waiting points for airplanes in different directions.
    - zero_point: Dictionary containing zero points for airplanes in different directions.
    - air_corridor: Dictionary containing air corridors for airplanes in different directions.
    - airplanes_list: Dictionary containing the list of airplanes currently at the airport.
    """

    def __init__(self):
        """
        Initializes an Airport object with default attributes.
        """
        self.airport_area = CustomSector(-5000, 5000, -5000, 5000, 0, 5000)
        self.initial_landing_point = {
                    "NW": CustomPoint(-2000, 450, 2000),
                    "NE": CustomPoint(2000, 450, 2000),
                    "SW": CustomPoint(-2000, -450, 2000),
                    "SE": CustomPoint(2000, -450, 2000)
        }
        self.waiting_point = {
                    "NW": CustomPoint(-3500, 1000, 2350),
                    "NE": CustomPoint(3500, 1000, 2350),
                    "SW": CustomPoint(-3500, -1000, 2350),
                    "SE": CustomPoint(3500, -1000, 2350)
        }
        self.zero_point = {
                    "N": CustomPoint(0, 450, 0),
                    "S": CustomPoint(0, -450, 0)
        }
        self.air_corridor = {
                    "N": AirCorridor("N"),
                    "S": AirCorridor("S")
        }
        self.airplanes_list = {}

    @staticmethod
    def establish_airplane_quarter(coordinates):
        """
        Determines the quarter in which the airplane is located based on its coordinates.

        Parameters:
        - coordinates: Dictionary containing the x, y, and z coordinates of the airplane.

        Returns:
        - A string representing the quarter in which the airplane is located.
        """
        if coordinates["x"] in range(-5000, 0) and coordinates["y"] in range(0, 5001):
             return "NW"
        elif coordinates["x"] in range(0, 5001) and coordinates["y"] in range(0, 5001):
            return "NE"
        elif coordinates["x"] in range(-5000, 0) and coordinates["y"] in range(-5000, 0):
            return "SW"
        elif coordinates["x"] in range(0, 5001) and coordinates["y"] in range(-5000, 0):
            return "SE"

    def check_distance_between_airplanes(self, airplane_object, airplane_id, airplanes_list):
        """
        Checks the distance between the given airplane and other airplanes in the list to prevent collisions.

        Parameters:
        - airplane_object: Dictionary containing details of the airplane.
        - airplane_id: The ID of the airplane to check.
        - airplanes_list: Dictionary containing details of all airplanes.

        Returns:
        - False if the airplane needs to avoid collision.
        - None if the airplanes have crashed.
        - True if everything is okay.
        """
        if len(airplanes_list) > 1:
            airplane_x = airplane_object[airplane_id]["coordinates"][0]
            airplane_y = airplane_object[airplane_id]["coordinates"][1]
            airplane_z = airplane_object[airplane_id]["coordinates"][2]
            for other_airplane, other_airplane_details in airplanes_list.items():
                if other_airplane != airplane_id:
                    other_airplane_x = other_airplane_details["coordinates"][0]
                    other_airplane_y = other_airplane_details["coordinates"][1]
                    other_airplane_z = other_airplane_details["coordinates"][2]
                    distance = euclidean_formula(airplane_x, airplane_y, airplane_z,
                                                 other_airplane_x, other_airplane_y, other_airplane_z)
                    if 300 < distance < 400:
                        return False
                    elif distance < 50:
                        return None
        return True


class Radar:
    """
    Represents a radar system for tracking airplanes within an airport.

    Attributes:
    - airport: The airport instance associated with the radar.
    - fig: The figure object for plotting.
    - ax: The axes object for 3D visualization.
    """

    def __init__(self, airport):
        """
        Initializes the Radar object with the given airport.

        Parameters:
        - airport: The airport instance associated with the radar.
        """
        self.airport = airport
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection = "3d")
        self.ax.set_xlim(-5000, 5000)
        self.ax.set_ylim(-5000, 5000)
        self.ax.set_zlim(0, 5000)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.ax.legend(loc = "upper left", bbox_to_anchor = (0.8, 0.8))

    def draw(self):
        """
        Draws the radar plot with airport landmarks and airplane positions.
        """
        self.ax.clear()
        points = {
            "Zero Point N": self.airport.zero_point["N"],
            "Zero Point S": self.airport.zero_point["S"]
        }
        for label, coordinates in points.items():
            x, y, z = coordinates.point_coordinates()
            self.ax.scatter(x, y, z, label = label, marker = "*", s = 100)
        if len(self.airport.airplanes_list) > 0:
            for airplane_id, airplane_details in list(self.airport.airplanes_list.items()):
                x = airplane_details["coordinates"][0]
                y = airplane_details["coordinates"][1]
                z = airplane_details["coordinates"][2]
                self.ax.scatter(x, y, z, label = airplane_id, marker = "^", s = 30)
        self.ax.legend(loc = "upper left", bbox_to_anchor = (0.8, 0.8))
        plt.draw()
        plt.pause(1)


class AirCorridor:
    """
    Represents an aerial corridor in a particular direction.

    Attributes:
    - direction (str): The direction of the corridor.
    - occupied (bool): Indicates whether the corridor is currently occupied by an airplane or not.
    """

    def __init__(self, direction):
        self.direction = direction
        self.occupied = False


class CustomSector:
    """
    Defines a custom sector in the airspace defined by its boundaries.

    Attributes:
    - x1, x2 (int): Boundaries along the x-axis.
    - y1, y2 (int): Boundaries along the y-axis.
    - z1, z2 (int): Boundaries along the z-axis.
    """

    def __init__(self, x1, x2, y1, y2, z1, z2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2


class CustomPoint:
    """
    Represents a point in the 3D space.

    Attributes:
    - x (int): The x-coordinate of the point.
    - y (int): The y-coordinate of the point.
    - z (int): The z-coordinate of the point.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def point_coordinates(self):
        """
        Returns the coordinates of the point as a tuple (x, y, z).
        """
        return (self.x, self.y, self.z)

