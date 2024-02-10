class CommunicationUtils:
    """
    A class containing utility method for communication protocols.
    """

    def protocol_template(self, message = None, body = None, **kwargs):
        """
        Generates a communication protocol template.

        Parameters:
        - message (str): The message to be included in the protocol template.
        - body (str): The body content of the protocol template.
        - **kwargs: Additional key-value pairs to be included in the protocol template.

        Returns:
        dict: A dictionary representing the communication protocol template.
        """
        template = {
            "message": message,
            "body": body,
            **kwargs
        }
        return template


class ServerProtocols(CommunicationUtils):
    """
    A class representing server-specific communication protocols.

    Inherits:
    - CommunicationUtils: Base class providing utility method for communication protocols.
    """

    def airport_is_full_message(self):
        """
        Generates a message indicating that the airport is full.

        Returns:
        dict: A communication protocol template indicating that the airport is full and the client needs to fly to another location.
        """
        return self.protocol_template(message = "Airport`s full: ", body = "You have to fly to another...")


class HandlerProtocols(CommunicationUtils):
    """
    A class representing handler-specific communication protocols.

    Inherits:
    - CommunicationUtils: Base class providing utility method for communication protocols.
    """

    def welcome_message_to_client(self, id):
        """
        Generates a welcome message to the client.

        Parameters:
        - id (str): The unique identifier of the client.

        Returns:
        dict: A communication protocol template welcoming the client and requesting their coordinates.
        """
        return self.protocol_template(message = "Welcome to our airport !", body = "Submit your coordinates", id = id)

    def points_for_airplane_message(self, quarter, init_point_coordinates, waiting_point_coordinates, zero_point_coordinates):
        """
        Generates a message containing points for airplane movement.

        Parameters:
        - quarter (str): The quarter where the airplane is located.
        - init_point_coordinates (dict): Initial landing point coordinates.
        - waiting_point_coordinates (dict): Waiting point coordinates.
        - zero_point_coordinates (dict): Zero point coordinates.

        Returns:
        dict: A communication protocol template providing points for airplane movement.
        """
        return self.protocol_template(message = "Your quarter: ",
                                      body = quarter,
                                      init_point_coordinates = init_point_coordinates,
                                      waiting_point_coordinates = waiting_point_coordinates,
                                      zero_point_coordinates = zero_point_coordinates)

    def direct_airplane_message(self, target):
        """
        Generates a message directing the airplane to a target location.

        Parameters:
        - target (str): The target location for the airplane.

        Returns:
        dict: A communication protocol template instructing the airplane to fly to a specific target.
        """
        return self.protocol_template(message = "Fly to: ", body = target)

    def avoid_collision_message(self):
        """
        Generates a message indicating that the airplane is too close to another airplane.

        Returns:
        dict: A communication protocol template advising the airplane to correct its flight path to avoid collision.
        """
        return self.protocol_template(message = "You`re to close to another airplane !", body = "Correct your flight")

    def collision_message(self):
        """
        Generates a message indicating that a collision has occurred.

        Returns:
        dict: A communication protocol template indicating that a collision has occurred and the airplane is destroyed.
        """
        return self.protocol_template(message = "Crash !", body = "R.I.P.")


class ClientProtocols(CommunicationUtils):
    """
    A class representing client-specific communication protocols.

    Inherits:
    - CommunicationUtils: Base class providing utility method for communication protocols.
    """

    def airplane_coordinates_message(self, coordinates):
        """
        Generates a message containing airplane coordinates.

        Parameters:
        - coordinates (dict): Dictionary containing airplane coordinates.

        Returns:
        dict: A communication protocol template indicating the airplane's coordinates.
        """
        return self.protocol_template(message = "Our coordinates: ", body = coordinates)

    def message_with_airplane_object(self, object):
        """
        Generates a message containing airplane data.

        Parameters:
        - object (dict): Dictionary containing airplane data.

        Returns:
        dict: A communication protocol template containing airplane data.
        """
        return self.protocol_template(message = "Our data: ", body = object)

    def reaching_the_target_message(self, target):
        """
        Generates a message indicating reaching the target.

        Parameters:
        - target (str): The target location reached by the airplane.

        Returns:
        dict: A communication protocol template indicating the airplane has reached the target.
        """
        return self.protocol_template(message = "We reached the target: ", body = target)

    def successfully_landing_message(self):
        """
        Generates a message indicating successful landing.

        Returns:
        dict: A communication protocol template indicating successful airplane landing.
        """
        return self.protocol_template(message = "Successfully landing", body = "Goodbye !")

    def out_of_fuel_message(self):
        """
        Generates a message indicating the airplane is out of fuel.

        Returns:
        dict: A communication protocol template indicating the airplane is out of fuel.
        """
        return self.protocol_template(message = "Out of fuel !", body = "We`re falling...")

    def crash_message(self):
        """
        Generates a message indicating a crash.

        Returns:
        dict: A communication protocol template indicating a crash has occurred.
        """
        return self.protocol_template(message = "Crash !", body = "Bye, bye...")
