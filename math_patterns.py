import math


def euclidean_formula(object_1, object_2):
    distance = math.sqrt((
        pow(object_1.x - object_2.x, 2) +
        pow(object_1.y - object_2.y, 2) +
        pow(object_1.z - object_2.z, 2)
    ))
    return distance

def simulating_airplane_movement(airplane, target, speed, time_interval):
    movement_to_target = True
    while movement_to_target:
        distance = euclidean_formula(airplane, target)
        if distance < speed * time_interval:
            movement_to_target = False
        else:
            delta_x = target.x - airplane.x
            delta_y = target.y - airplane.y
            delta_z = target.z - airplane.z
            angle_xy = math.atan2(delta_y, delta_x)
            angle_xz = math.atan2(delta_z, math.sqrt(pow(delta_x, 2) + pow(delta_y, 2)))
            v_x = speed * math.cos(angle_xy) * math.cos(angle_xz)
            v_y = speed * math.sin(angle_xy) * math.cos(angle_xz)
            v_z = speed * math.sin(angle_xz)
            airplane.x += v_x * time_interval
            airplane.y += v_y * time_interval
            airplane.z += v_z * time_interval

def simulating_landing(airport, airplane):
    simulating_airplane_movement(airplane, airport.zero_point, airplane.speed, 1)
    if 0 <= airplane.z <= 50:
        return True
    elif airplane.z < 0:
        return False


