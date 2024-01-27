from math_patterns import movement_formula
from airport import Airport
import time
from airplane import Airplane
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



init_coords_1 = Airplane.establish_init_airplane_coordinates()
init_coords_2 = Airplane.establish_init_airplane_coordinates()
airplane_obj_1 = Airplane(init_coords_1)
airplane_obj_2 = Airplane(init_coords_2)

a_list = []
a_list.append(airplane_obj_1)
a_list.append(airplane_obj_2)




# airport_scatter = ax.scatter(*airport_coords, color='red', label='Airport')
# airplane_scatters = []  # Lista do przechowywania obiektów scatter dla samolotów
#
# for a in a_list:
#     airplane_scatter = ax.scatter(a.x, a.y, a.z, marker='o', label="Airplane")
#     airplane_scatters.append(airplane_scatter)
fig = plt.figure()


def asd():

    # global a_list
    ax = fig.add_subplot(111, projection='3d')
    # Usunięcie wszystkich punktów z wykresu
    ax.clear()
    airport_coords = (0, 0, 0)
    ax.set_xlim([-5000, 5000])
    ax.set_ylim([-5000, 5000])
    ax.set_zlim([0, 5000])

    # Dodanie lotniska
    ax.scatter(*airport_coords, color='red', label='Airport')

    # Dodanie nowych punktów dla każdego samolotu
    for a in a_list:
        ax.scatter(a.x, a.y, a.z, marker='o', label="Airplane")

    ax.legend()
    plt.draw()


i = 0
while i < 10:
    asd()
    for airplane in a_list:
        movement_formula(airplane, 0, 0, 0)
    if i == 5:
        init_coords_3 = Airplane.establish_init_airplane_coordinates()
        airplane_obj_3 = Airplane(init_coords_3)
        a_list.append(airplane_obj_3)
    plt.pause(1)
    i += 1


