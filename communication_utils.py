class CommunicationUtils:
    def protocol_template(self, message = "null", body = "null"):
        template = {
            "message": message,
            "body": body
        }
        return template


class ServerProtocols(CommunicationUtils):
    def welcome_protocol(self):
        self.protocol_template(message = "Welcome", body = "Submit your coordinates")


class ClientProtocols(CommunicationUtils):
    def initial_coordinates(self, coordinates):
        self.protocol_template(message = "Coordinates", body = coordinates)
