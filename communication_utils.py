class CommunicationUtils:
    def protocol_template(self, message = None, body = None, **kwargs):
        template = {
            "message": message,
            "body": body,
            **kwargs
        }
        return template


class ServerProtocols(CommunicationUtils):
    def welcome_protocol(self, id):
        return self.protocol_template(message = "Welcome to our airport !", body = "Submit your coordinates", id = id)

    def points_for_airplane_protocol(self, points):
        return self.protocol_template(message = "Your points: ", body = points)

class ClientProtocols(CommunicationUtils):
    def send_coordinates_protocol(self, coordinates):
        return self.protocol_template(message = "Our coordinates: ", body = coordinates)

    def send_airplane_object_protocol(self, object):
        return self.protocol_template(message = "Our data: ", body = object)
