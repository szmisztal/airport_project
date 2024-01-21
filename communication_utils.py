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

    def direct_airplane_protocol(self, target, coordinates):
        return self.protocol_template(message = "Fly to: ", body = target, coordinates = coordinates)

    def airport_full_protocol(self):
        return self.protocol_template(message = "Airport`s full: ", body = "You have to fly to another...")


class ClientProtocols(CommunicationUtils):
    def coordinates_protocol(self, coordinates):
        return self.protocol_template(message = "Our coordinates: ", body = coordinates)

    def airplane_object_protocol(self, object):
        return self.protocol_template(message = "Our data: ", body = object)

    def reaching_the_target_protocol(self, target):
        return self.protocol_template(message = "We reached the target: ", body = target)

    def successfully_landing_protocol(self):
        return self.protocol_template(message = "Successfully landing", body = "Goodbye !")

    def out_of_fuel_protocol(self):
        return self.protocol_template(message = "Out of fuel !", body = "We`re falling...")
