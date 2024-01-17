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

    def direct_airplane_protocol(self, point):
        return self.protocol_template(message = "Fly to: ", body = point)


class ClientProtocols(CommunicationUtils):
    def coordinates_protocol(self, coordinates):
        return self.protocol_template(message = "Our coordinates: ", body = coordinates)

    def airplane_object_protocol(self, object):
        return self.protocol_template(message = "Our data: ", body = object)
