import math


def euclidean_formula(airplane_x, airplane_y, airplane_z, target_x, target_y, target_z):
    distance = math.sqrt((
        pow(airplane_x - target_x, 2) +
        pow(airplane_y - target_y, 2) +
        pow(airplane_z - target_z, 2)
    ))
    return round(distance)

def movement_formula(airplane, target_x, target_y, target_z):
    delta_x = target_x - airplane.x
    delta_y = target_y - airplane.y
    delta_z = target_z - airplane.z
    angle_xy = math.atan2(delta_y, delta_x)
    angle_xz = math.atan2(delta_z, math.sqrt(pow(delta_x, 2) + pow(delta_y, 2)))
    v_x = airplane.speed * math.cos(angle_xy) * math.cos(angle_xz)
    v_y = airplane.speed * math.sin(angle_xy) * math.cos(angle_xz)
    v_z = airplane.speed * math.sin(angle_xz)
    airplane.x += round(v_x)
    airplane.y += round(v_y)
    airplane.z += round(v_z)
