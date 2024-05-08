class MessageTemplate:
    """
    A class used to create a standard message template for communications.

    Attributes:
        status (dict): A dictionary holding the possible statuses of messages
                       such as 'success_status' and 'error_status'.

    Methods:
        protocol_template(status, message, data=None):
            Constructs a dictionary that formats a message according to a specified
            protocol with a status, an optional message, and optional data.
    """

    def __init__(self):
        """
        Initialize the MessageTemplate with predefined statuses.
        """
        self.status = {
            "success_status": "SUCCESS",
            "error_status": "ERROR"

        }

    def protocol_template(self, status, message, data = None):
        """
        Generate a formatted message template.

        Parameters:
            status (str): The status of the message, usually indicating success or error.
            message (str): The main content of the message.
            data (any, optional): Additional data relevant to the message. Defaults to None.

        Returns:
            dict: A dictionary containing the formatted message.
        """
        template = {
            "status": status,
            "message": message,
            "data": data,
        }
        return template
