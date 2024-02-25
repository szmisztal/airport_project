import pytest
from server_side.airport import Airport


@pytest.fixture
def init_airport_obj():
    airport = Airport()
    return airport

@pytest.fixture
def airplane_object():
    airplane_object = {"Airplane_1": {"coordinates": [2000, 3000, 1500]}}
    return airplane_object


def test_airport_init(init_airport_obj):
    airport = init_airport_obj
    assert airport.airport_area.x1 == -5000
    assert airport.airport_area.x2 == 5000
    assert airport.airport_area.y1 == -5000
    assert airport.airport_area.y2 == 5000
    assert airport.airport_area.z1 == 0
    assert airport.airport_area.z2 == 5000
    assert airport.initial_landing_point["NW"].point_coordinates() == (-2000, 450, 2000)
    assert airport.initial_landing_point["NE"].point_coordinates() == (2000, 450, 2000)
    assert airport.initial_landing_point["SW"].point_coordinates() == (-2000, -450, 2000)
    assert airport.initial_landing_point["SE"].point_coordinates() == (2000, -450, 2000)
    assert airport.waiting_point["NW"].point_coordinates() == (-3500, 1000, 2350)
    assert airport.waiting_point["NE"].point_coordinates() == (3500, 1000, 2350)
    assert airport.waiting_point["SW"].point_coordinates() == (-3500, -1000, 2350)
    assert airport.waiting_point["SE"].point_coordinates() == (3500, -1000, 2350)
    assert airport.zero_point["N"].point_coordinates() == (0, 450, 0)
    assert airport.zero_point["S"].point_coordinates() == (0, -450, 0)
    assert airport.air_corridor["N"].direction == "N"
    assert airport.air_corridor["N"].occupied == False
    assert airport.air_corridor["S"].direction == "S"
    assert airport.air_corridor["S"].occupied == False
    assert len(airport.airplanes_list) == 0


@pytest.mark.parametrize("coordinates, result", [
    ({"x": -4400, "y": 3500}, "NW"),
    ({"x": 3678, "y": 4754}, "NE"),
    ({"x": -3678, "y": -4754}, "SW"),
    ({"x": 3678, "y": -4754}, "SE"),
    ({"x": 5500, "y": 0}, None),
    ({"x": 0, "y": -5002}, None),
    ({"x": 5500, "y": -5500}, None)
])
def test_establish_airplane_quarter(coordinates, result):
    assert Airport.establish_airplane_quarter(coordinates) == result


@pytest.mark.parametrize("other_airplane_to_check_distance, result", [
    ({"Airplane_2": {"coordinates": [2001, 3001, 1501]}, "Airplane_3": {"coordinates": [-2000, -3000, 1500]}}, None),
    ({"Airplane_2": {"coordinates": [-2000, -3000, 1470]}, "Airplane_3": {"coordinates": [2000, 3000, 1150]}}, False),
    ({"Airplane_2": {"coordinates": [-2000, -3000, 1150]}, "Airplane_3": {"coordinates": [5000, 5000, 2500]}}, True)
])
def test_check_distance_between_airplanes(init_airport_obj, airplane_object, other_airplane_to_check_distance, result):
    airport = init_airport_obj
    airplane = airplane_object
    assert airport.check_distance_between_airplanes(airplane, "Airplane_1", other_airplane_to_check_distance) == result

