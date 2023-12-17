from itertools import product
import time
import math_patterns
from airport import Airport
from airplane import Airplane
# from connection_pool import ConnectionPool
from math_patterns import simulating_airplane_movement
# conn = ConnectionPool(10, 100)
# print(conn.connections_list)


a = Airplane.establish_init_airplane_coordinates()
b = Airplane.establish_init_airplane_coordinates()
airport = Airport()
airport.create_airplane_object_and_append_it_to_list(a)
airport.create_airplane_object_and_append_it_to_list(b)
airplane_1 = airport.airplanes_in_the_air_list[0]
airplane_2 = airport.airplanes_in_the_air_list[1]
movement = True
while movement:
    math_patterns.simulating_airplane_movement(airplane_1, airport.zero_point_N)
    math_patterns.simulating_airplane_movement(airplane_2, airport.zero_point_S)
    print(airplane_1.coordinates)
    print(airplane_2.coordinates)
    time.sleep(1)
    if airplane_1.x == 4000 or airplane_1.y == 4000 or airplane_1.z == 2000 or airplane_2.y == 4000 or airplane_2.y == 4000 or airplane_2.z == 2000:
        movement = False

