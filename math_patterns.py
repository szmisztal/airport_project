import math


def euclidean_formula(object_1, object_2):
    distance = math.sqrt((
        pow(object_1.x - object_2.x, 2) +
        pow(object_1.y - object_2.y, 2) +
        pow(object_1.z - object_2.z, 2)
    ))
    return distance

def simulating_airplane_movement(airplane, target, speed, time_interval, comment = None):
    current_position = airplane
    while True:
        distance = euclidean_formula(airplane, target)
        if distance < speed * time_interval:
            if comment:
                print(comment)
            break
        else:
            delta_x = target.x - current_position.x
            delta_y = target.y - current_position.y
            delta_z = target.z - current_position.z
            angle_xy = math.atan2(delta_y, delta_x)
            angle_xz = math.atan2(delta_z, math.sqrt(pow(delta_x, 2) + pow(delta_y, 2)))
            v_x = speed * math.cos(angle_xy) * math.cos(angle_xz)
            v_y = speed * math.sin(angle_xy) * math.cos(angle_xz)
            v_z = speed * math.sin(angle_xz)
            current_position.x += v_x * time_interval
            current_position.y += v_y * time_interval
            current_position.z += v_z * time_interval
            print(f"X: {current_position.x:.2f}, Y: {current_position.y:.2f}, Z: {current_position.z:.2f}")

def simulating_landing(airport, airplane):
    simulating_airplane_movement(airplane, airport.zero_point, 200, 1)


