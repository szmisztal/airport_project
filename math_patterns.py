import math


def euclidean_formula(object_1, object_2):
    distance = math.sqrt((
        pow(object_1.x - object_2.x, 2) +
        pow(object_1.y - object_2.y, 2) +
        pow(object_1.z - object_2.z, 2)
    ))
    return round(distance)

def movement_formula(airplane, target_x, target_y, target_z, time_interval = 1):
    delta_x = target_x - airplane.x
    delta_y = target_y - airplane.y
    delta_z = target_z - airplane.z
    angle_xy = math.atan2(delta_y, delta_x)
    angle_xz = math.atan2(delta_z, math.sqrt(pow(delta_x, 2) + pow(delta_y, 2)))
    v_x = airplane.speed * math.cos(angle_xy) * math.cos(angle_xz)
    v_y = airplane.speed * math.sin(angle_xy) * math.cos(angle_xz)
    v_z = airplane.speed * math.sin(angle_xz)
    airplane.x += round(v_x * time_interval)
    airplane.y += round(v_y * time_interval)
    airplane.z += round(v_z * time_interval)
