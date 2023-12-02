import math_patterns
from airplane import Airplane
from airport import Airport

init = Airplane.establish_init_airplane_coordinates()
airplane = Airplane(**init)
airport = Airport()

def xyz(airplane, airport):
    math_patterns.simulating_airplane_movement(airplane, airport.starting_landing_point_NW, airplane.speed, 1)
    math_patterns.simulating_landing(airport, airplane, "N")

xyz(airplane, airport)
