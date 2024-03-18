import requests


class AdminCommands:
    def __init__(self):
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
        response = requests.post("http://127.0.0.1:5000/",
                                 json = {"jsonrpc": "2.0",
                                         "method": method,
                                         "params": kwargs,
                                         "id": method_id}
                                 )
        return response.json()

    def start_airport(self):
        return self.request_template("server_start", 1)

    def close_airport(self):
        return self.request_template("server_close", 2)

    def pause_airport(self):
        return self.request_template("server_pause", 3)

    def resume_airport(self):
        return self.request_template("server_resume", 4)

    def airport_uptime(self):
        return self.request_template("server_uptime", 5)

    def airplanes_number(self):
        return self.request_template("number_of_airplanes", 6)

    def airplane_details(self):
        try:
            id = int(input("Airplane id: "))
            return self.request_template("single_airplane_details", 7, id = id)
        except TypeError as e:
            print(f"{e} - try again")

    def airplanes_in_the_air(self):
        return self.request_template("airplanes_by_status", 8, status = None)

    def airplanes_successfully_landed(self):
        return self.request_template("airplanes_by_status", 9, status = "SUCCESSFULLY LANDING")

    def airplanes_crashed_by_out_of_fuel(self):
        return self.request_template("airplanes_by_status", 10, status = "CRASHED BY OUT OF FUEL")

    def airplanes_crashed_by_collisions(self):
        return self.request_template("airplanes_by_status", 11, status = "CRASHED BY COLLISION")

    def main(self):
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

