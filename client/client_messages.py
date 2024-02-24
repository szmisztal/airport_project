from server.server_messages import CommunicationUtils


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
