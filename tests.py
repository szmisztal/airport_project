from itertools import product
import time
import math_patterns
from airport import Airport
from airplane import Airplane
from connection_pool import ConnectionPool
from math_patterns import movement_formula, euclidean_formula
# conn = ConnectionPool(10, 100)
# print(conn.connections_list)


a = Airplane.establish_init_airplane_coordinates()
b = Airplane.establish_init_airplane_coordinates()
airport = Airport()
airport.create_airplane_object_and_append_it_to_list(a, 0)
airport.create_airplane_object_and_append_it_to_list(b, 1)
airplane_1 = airport.airplanes_in_the_air_list[0]
airplane_2 = airport.airplanes_in_the_air_list[1]
movement = True
while movement:
    airport.airport_manager()
    # print(airplane_1.x, airplane_1.y, airplane_1.z)
    print(airplane_1.move_to_initial_landing_point, airplane_1.move_to_waiting_sector, airplane_1.move_to_runaway)
    # time.sleep(1)



