from common.message_template import MessageTemplate


class ServerProtocols(MessageTemplate):
    """
    A class representing server_side-specific communication protocols.

    Inherits:
    - MessageTemplate: Base class providing utility method for communication protocols.
    """
    def __init__(self):
        super().__init__()

    def airport_is_full_message(self):
        """
        Generates a message indicating that the airport is full.

        Returns:
        dict: A communication protocol template indicating that the airport is full and the client_side needs to fly to another location.
        """
        return self.protocol_template(status = self.status["error_status"], message = "Airport`s full, you have to fly to another...")


class HandlerProtocols(MessageTemplate):
    """
    A class representing handler-specific communication protocols.

    Inherits:
    - MessageTemplate: Base class providing utility method for communication protocols.
    """
    def __init__(self):
        super().__init__()

    def welcome_message_to_client(self, id):
        """
        Generates a welcome message to the client_side.

        Parameters:
        - id (str): The unique identifier of the client_side.

        Returns:
        dict: A communication protocol template welcoming the client_side and requesting their coordinates.
        """
        return self.protocol_template(status = self.status["success_status"] , message = "Welcome to our airport !", data = id)

    def points_for_airplane_message(self, quarter, init_landing_point_coordinates, waiting_point_coordinates, zero_point_coordinates):
        """
        Generates a message containing points for airplane movement.

        Parameters:
        - quarter (str): The quarter where the airplane is located.
        - init_landing_point_coordinates (dict): Initial landing point coordinates.
        - waiting_point_coordinates (dict): Waiting point coordinates.
        - zero_point_coordinates (dict): Zero point coordinates.

        Returns:
        dict: A communication protocol template providing points for airplane movement.
        """
        return self.protocol_template(status = self.status["success_status"],
                                      message = "Your coordinates points: ",
                                      data = {
                                          "quarter": quarter,
                                          "init_landing_point_coordinates": init_landing_point_coordinates,
                                          "waiting_point_coordinates": waiting_point_coordinates,
                                          "zero_point_coordinates": zero_point_coordinates
                                      })

    def direct_airplane_message(self, target):
        """
        Generates a message directing the airplane to a target location.

        Parameters:
        - target (str): The target location for the airplane.

        Returns:
        dict: A communication protocol template instructing the airplane to fly to a specific target.
        """
        return self.protocol_template(status = self.status["success_status"], message = "Fly to: ", data = target)

    def avoid_collision_message(self):
        """
        Generates a message indicating that the airplane is too close to another airplane.

        Returns:
        dict: A communication protocol template advising the airplane to correct its flight path to avoid collision.
        """
        return self.protocol_template(status = self.status["error_status"], message = "You`re to close to another airplane ! Correct your flight.")

    def collision_message(self):
        """
        Generates a message indicating that a collision has occurred.

        Returns:
        dict: A communication protocol template indicating that a collision has occurred and the airplane is destroyed.
        """
        return self.protocol_template(status = self.status["error_status"], message = "Crash !...")
