import math
from airplane import Airplane

init_coords = Airplane.establish_init_airplane_coordinates()
airplane = Airplane(**init_coords)
print(airplane)
print(airplane.quarter)

