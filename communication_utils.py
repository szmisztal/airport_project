class CommunicationUtils:
    def protocol_template(self, message = "null", body = "null"):
        template = {
            "message": message,
            "body": body
        }
        return template


class ServerProtocols(CommunicationUtils):
    def welcome_protocol(self):
        return self.protocol_template(message = "Welcome", body = "Submit your coordinates")

    def airplane_crashed(self):
        return self.protocol_template(message = "Crash !", body = "Airplane`s destroyed...")

    def successfully_landing(self):
        return self.protocol_template(message = "Success !", body = "You`re successfully landing")


class ClientProtocols(CommunicationUtils):
    def initial_coordinates(self, coordinates):
        return self.protocol_template(message = "Coordinates", body = coordinates)
