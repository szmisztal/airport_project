import os

import requests


class AdminCommands:
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


if __name__ == "__main__":
    commands = AdminCommands()
    response = commands.start_airport()
    print(response)

