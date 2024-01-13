import matplotlib.pyplot as plt
from airplane import Airplane

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

airplane_1 = {
    "Airplane_1": {
        "coordinates": [5000, 2000, 2500],
        "quarter": "NW",
        "initial_landing_point": "NW",
        "waiting_sector": "NW",
        "zero_point": "N"
    }
}

airplane_2 = {
    "Airplane_2": {
        "coordinates": [-5000, -2000, 3000],
        "quarter": "SE",
        "initial_landing_point": "SE",
        "waiting_sector": "SE",
        "zero_point": "S"
    }
}

# airplanes = {}
# airplanes.update(airplane_1)
# airplanes.update(airplane_2)
#
# for _ in range(10):
#     for key, value in airplanes.items():
#         for sub_key, sub_value in value.items():
#             if sub_key == "coordinates":
#                 sub_value = [coord + 500 for coord in sub_value]
#                 print(sub_value)
#                 airplanes[key][sub_key] = sub_value


airplanes = []
airplanes.append(airplane_1)
airplanes.append(airplane_2)

for item in airplanes:
    for airplane, airplane_details in item.items():
        for detail_key, detail_value in airplane_details.items():
            if detail_key == "coordinates":
                detail_value = [coord + 500 for coord in detail_value]
                print(detail_value)
                airplane_details["coordinates"] = detail_value

print(airplanes)

