from common.message_template import MessageTemplate


class ClientProtocols(MessageTemplate):
    """
    A class representing client_side-specific communication protocols.

    Inherits:
    - MessageTemplate: Base class providing utility method for communication protocols.
    """
    def __init__(self):
        super().__init__()

    def airplane_coordinates_message(self, coordinates):
        """
        Generates a message containing airplane coordinates.

        Parameters:
        - coordinates (dict): Dictionary containing airplane coordinates.

        Returns:
        dict: A communication protocol template indicating the airplane's coordinates.
        """
        return self.protocol_template(status = self.status["success_status"], message = "Our coordinates: ", data = coordinates)

    def message_with_airplane_object(self, object):
        """
        Generates a message containing airplane data.

        Parameters:
        - object (dict): Dictionary containing airplane data.

        Returns:
        dict: A communication protocol template containing airplane data.
        """
        return self.protocol_template(status = self.status["success_status"], message = "Our data: ", data = object)

    def reaching_the_target_message(self, target):
        """
        Generates a message indicating reaching the target.

        Parameters:
        - target (str): The target location reached by the airplane.

        Returns:
        dict: A communication protocol template indicating the airplane has reached the target.
        """
        return self.protocol_template(status = self.status["success_status"], message = "We reached the target: ", data = target)

    def successfully_landing_message(self):
        """
        Generates a message indicating successful landing.

        Returns:
        dict: A communication protocol template indicating successful airplane landing.
        """
        return self.protocol_template(status = self.status["success_status"], message = "We was successfully landed")

    def out_of_fuel_message(self):
        """
        Generates a message indicating the airplane is out of fuel.

        Returns:
        dict: A communication protocol template indicating the airplane is out of fuel.
        """
        return self.protocol_template(status = self.status["error_status"], message = "Out of fuel ! We`re falling...")

    def crash_message(self):
        """
        Generates a message indicating a crash.

        Returns:
        dict: A communication protocol template indicating a crash has occurred.
        """
        return self.protocol_template(status = self.status["error_status"], message = "Crash ! Bye, bye...")
