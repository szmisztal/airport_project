import requests


class AdminCommands:
    """
    A class to manage administrative commands for controlling an airport server.

    Attributes:
        is_running (bool): Indicates if the command interface is active.
        commands_list (dict): A dictionary mapping command numbers to their descriptions.
    """
    def __init__(self):
        """
        Initializes the AdminCommands class with default values.
        """
        self.is_running = True
        self.commands_list = {
            "1": "Start airport",
            "2": "Close airport",
            "3": "Pause airport",
            "4": "Resume airport",
            "5": "Airport uptime",
            "6": "Airplanes number",
            "7": "Airplane details",
            "8": "Airplanes actually in the air",
            "9": "Airplanes successfully landed",
            "10": "Airplanes crashed by out of fuel",
            "11": "Airplanes crashed by collisions",
            "12": "Stop"
        }

    def request_template(self, method, method_id, **kwargs):
        """
        Sends a JSON-RPC request to the airport server.

        Args:
            method (str): The method name to be called on the server.
            method_id (int): An identifier for the method call.
            **kwargs: Arbitrary keyword arguments that are passed to the method.

        Returns:
            dict: The JSON response from the server.
        """
        response = requests.post("http://127.0.0.1:5000/",
                                 json = {"jsonrpc": "2.0",
                                         "method": method,
                                         "params": kwargs,
                                         "id": method_id}
                                 )
        return response.json()

    def start_airport(self):
        """
        Sends a request to start the airport server.

        Returns:
            dict: The JSON response from the server indicating the start status.
        """
        return self.request_template("server_start", 1)

    def close_airport(self):
        """
        Sends a request to close the airport server.

        Returns:
            dict: The JSON response from the server indicating the close status.
        """
        return self.request_template("server_close", 2)

    def pause_airport(self):
        """
        Sends a request to pause the airport server.

        Returns:
            dict: The JSON response from the server indicating the pause status.
        """
        return self.request_template("server_pause", 3)

    def resume_airport(self):
        """
        Sends a request to resume the airport server.

        Returns:
            dict: The JSON response from the server indicating the resume status.
        """
        return self.request_template("server_resume", 4)

    def airport_uptime(self):
        """
        Requests the current uptime of the airport server.

        Returns:
            dict: The JSON response from the server indicating the server's uptime.
        """
        return self.request_template("server_uptime", 5)

    def airplanes_number(self):
        """
        Requests the number of airplanes processed by the airport server.

        Returns:
            dict: The JSON response from the server with the number of airplanes.
        """
        return self.request_template("number_of_airplanes", 6)

    def airplane_details(self):
        """
        Requests the details of a specific airplane by its ID.

        Returns:
            dict: The JSON response from the server with the airplane details or an error message.
        """
        try:
            id = int(input("Airplane id: "))
            return self.request_template("single_airplane_details", 7, id = id)
        except TypeError as e:
            print(f"{e} - try again")

    def airplanes_in_the_air(self):
        """
        Requests the list of airplanes that are currently in the air.

        Returns:
            dict: The JSON response from the server with the list of airplanes in the air.
        """
        return self.request_template("airplanes_by_status", 8, status = None)

    def airplanes_successfully_landed(self):
        """
        Requests the list of airplanes that have successfully landed.

        Returns:
            dict: The JSON response from the server with the list of successfully landed airplanes.
        """
        return self.request_template("airplanes_by_status", 9, status = "SUCCESSFULLY LANDING")

    def airplanes_crashed_by_out_of_fuel(self):
        """
        Requests the list of airplanes that have crashed due to running out of fuel.

        Returns:
            dict: The JSON response from the server with the list of airplanes crashed by fuel exhaustion.
        """
        return self.request_template("airplanes_by_status", 10, status = "CRASHED BY OUT OF FUEL")

    def airplanes_crashed_by_collisions(self):
        """
        Requests the list of airplanes that have crashed due to collisions.

        Returns:
            dict: The JSON response from the server with the list of airplanes crashed by collisions.
        """
        return self.request_template("airplanes_by_status", 11, status = "CRASHED BY COLLISION")

    def main(self):
        """
        The main loop for processing user commands. It displays available commands and processes user input.
        """
        response = None
        for key, value in self.commands_list.items():
            print(f"{key}: {value}")
        while self.is_running:
            command = input("Choose command number: ")
            if command == "1":
                response = self.start_airport()
            elif command == "2":
                response = self.close_airport()
            elif command == "3":
                response = self.pause_airport()
            elif command == "4":
                response = self.resume_airport()
            elif command == "5":
                response = self.airport_uptime()
            elif command == "6":
                response = self.airplanes_number()
            elif command == "7":
                response = self.airplane_details()
            elif command == "8":
                response = self.airplanes_in_the_air()
            elif command == "9":
                response = self.airplanes_successfully_landed()
            elif command == "10":
                response = self.airplanes_crashed_by_out_of_fuel()
            elif command == "11":
                response = self.airplanes_crashed_by_collisions()
            elif command == "12":
                self.close_airport()
                print("Bye !")
                self.is_running = False
            else:
                response = "Wrong command, try again"
            print(response)


if __name__ == "__main__":
    commands = AdminCommands()
    commands.main()

