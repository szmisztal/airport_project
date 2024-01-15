import matplotlib.pyplot as plt
from airplane import Airplane
from math_patterns import movement_formula
from airport import Airport
import time


# airport_coords = (0, 0, 0)
#
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
#
# ax.set_xlim([-5000, 5000])
# ax.set_ylim([-5000, 5000])
# ax.set_zlim([0, 5000])
#
# ax.scatter(*airport_coords, color='red', label='Airport')

# airplanes = {
#     'airplane_1': [1000, 1000, 5000],
#     'airplane_2': [-2000, 1500, 500],
#     'airplane_3': [3000, -3000, 2000]
#     }

# airplanes_test = {}
# airplane_obj_1 = Airplane({'x': 5000, 'y': 3000, 'z': 200})
# airplane_obj_1.id = 1
# airplane = {f'Airplane_{airplane_obj_1.id}': [airplane_obj_1.x, airplane_obj_1.y, airplane_obj_1.z]}
# airplanes_test.update(airplane)
#
# airplane_obj_2 = Airplane({'x': -5000, 'y': -3000, 'z': 200})
# airplane_obj_2.id = 2
# airplane_2 = {f'Airplane_{airplane_obj_2.id}': [airplane_obj_2.x, airplane_obj_2.y, airplane_obj_2.z]}
# airplanes_test.update(airplane_2)

# for key, value in airplanes_test.items():
#     ax.scatter(value[0], value[1], value[2], marker = 'o', label = key)
#
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
#
# ax.legend()
#
# for i in range(10):
#     for key, value in airplanes_test.items():
#         value[0] += 500
#         value[1] += 500
#         value[2] += 100
#     plt.pause(1)
#     ax.clear()
#     ax.scatter(*airport_coords, color='red', label='Airport')
#     for key, value in airplanes_test.items():
#         ax.scatter(value[0], value[1], value[2], marker='o', label=key)
#     ax.set_xlim([-5000, 5000])
#     ax.set_ylim([-5000, 5000])
#     ax.set_zlim([0, 5000])
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')
#     ax.legend()
#     plt.draw()
#
# plt.show()
a = Airplane(Airplane.establish_init_airplane_coordinates())
print(a.quarter, a.zero_point, a.waiting_point, a.initial_landing_point)
b = a.parse_airplane_obj_to_json()
print(b)
update_data = {'quarter': 'NW','initial_landing_point': 'NW', 'waiting_point': 'NW', 'zero_point': 'N'}
b["Airplane_None"].update(update_data)
print(b)
a.quarter = update_data.get("quarter")
a.initial_landing_point = update_data.get("initial_landing_point")
a.waiting_point = update_data.get("waiting_point")
a.zero_point = update_data.get("zero_point")

print(a.quarter, a.zero_point, a.waiting_point, a.initial_landing_point)
