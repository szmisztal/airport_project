import datetime
import time
import schedule
from client import Client


class Airplane:
    def __init__(self, x, y, z):
        self.client = Client()
        self.date_of_appearance = datetime.datetime.now()
        self.x = x
        self.y = y
        self.z = z
        self.fuel_reserve = 3
        self.co_ordinates = (x, y, z)
        self.manager = self.airplane_manager()

    def fuel_consumption_per_hour(self):
        self.fuel_reserve -= 1
        if self.fuel_reserve == 0:
            print("Out of fuel ! Airplane destroyed...")
            self.client.stop()

    def airplane_axis_movement(self, axis):
        if axis == self.x or axis == self.y:
            if axis < 0:
                if axis == self.x:
                    self.x += 200
                elif axis == self.y:
                    self.y += 200
            elif axis > 0:
                if axis == self.x:
                    self.x -= 200
                elif axis == self.y:
                    self.y -= 200
        elif axis == self.z:
            self.z -= 20
        return (self.x, self.y, self.z)

    def simulate_airplane_movement(self):
        self.airplane_axis_movement(self.x)
        self.airplane_axis_movement(self.y)
        self.airplane_axis_movement(self.z)

    def airplane_manager(self):
        schedule.every(1).hour.do(self.fuel_consumption_per_hour)
        schedule.every(1).second.do(self.simulate_airplane_movement)
        # while True:
        #     schedule.run_pending()

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"
