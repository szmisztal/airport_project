class CommunicationUtils:
    def protocol_template(self, message = None, body = None, id = None):
        template = {
            "message": message,
            "body": body,
            "id": id
        }
        return template


class ServerProtocols(CommunicationUtils):
    def welcome_protocol(self, id):
        return self.protocol_template(message = "Welcome to our airport !", body = "Submit your coordinates", id = id)

    def airplane_crashed(self):
        return self.protocol_template(message = "Crash !", body = "Airplane crashed..")

    def successfully_landing(self):
        return self.protocol_template(message = "Success !", body = "You`re successfully landed")

    def server_shut_down(self):
        return self.protocol_template(message = "Server status:", body = "Shutting down..")

    def connections_limit(self):
        return self.protocol_template(message = "Airport`s full:", body = "You have to fly away..")


class ClientProtocols(CommunicationUtils):
    def initial_coordinates(self, coordinates):
        return self.protocol_template(message = "Coordinates", body = coordinates)
