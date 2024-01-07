import matplotlib.pyplot as plt

airport_coords = (0, 0, 0)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlim([-5000, 5000])
ax.set_ylim([-5000, 5000])
ax.set_zlim([0, 5000])

ax.scatter(*airport_coords, color='red', label='Airport')

airplanes = [(1000, 1000, 5000), (-2000, 1500, 5000), (3000, -3000, 2000)]

for idx, (x, y, z) in enumerate(airplanes):
    ax.scatter(x, y, z, marker='o', label=f'Airplane {idx+1}')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.legend()
plt.show()
