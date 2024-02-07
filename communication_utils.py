class CommunicationUtils:
    def protocol_template(self, message = None, body = None, **kwargs):
        template = {
            "message": message,
            "body": body,
            **kwargs
        }
        return template


class ServerProtocols(CommunicationUtils):
    def airport_is_full_message(self):
        return self.protocol_template(message = "Airport`s full: ", body = "You have to fly to another...")


class HandlerProtocols(CommunicationUtils):
    def welcome_message_to_client(self, id):
        return self.protocol_template(message = "Welcome to our airport !", body = "Submit your coordinates", id = id)

    def points_for_airplane_message(self, points):
        return self.protocol_template(message = "Your points: ", body = points)

    def direct_airplane_message(self, target, coordinates):
        return self.protocol_template(message = "Fly to: ", body = target, coordinates = coordinates)

    def avoid_collision_message(self):
        return self.protocol_template(message = "You`re to close to another airplane !", body = "Correct your flight")

    def collision_message(self):
        return self.protocol_template(message = "Crash !", body = "R.I.P.")


class ClientProtocols(CommunicationUtils):
    def airplane_coordinates_message(self, coordinates):
        return self.protocol_template(message = "Our coordinates: ", body = coordinates)

    def message_with_airplane_object(self, object):
        return self.protocol_template(message = "Our data: ", body = object)

    def reaching_the_target_message(self, target):
        return self.protocol_template(message = "We reached the target: ", body = target)

    def successfully_landing_message(self):
        return self.protocol_template(message = "Successfully landing", body = "Goodbye !")

    def out_of_fuel_message(self):
        return self.protocol_template(message = "Out of fuel !", body = "We`re falling...")
