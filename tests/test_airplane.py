import pytest
import datetime
from unittest.mock import patch
from airplane import Airplane


@pytest.fixture
def init_airplane_obj(mocker):
    mock_client = mocker.Mock()
    coordinates = {"x": -5000, "y": 3500, "z": 4400}
    airplane = Airplane(mock_client, coordinates)
    return airplane

def test_airplane_init(init_airplane_obj):
    airplane = init_airplane_obj
    assert airplane.id == None
    assert airplane.x == -5000
    assert airplane.y == 3500
    assert airplane.z == 4400
    assert airplane.quarter == None
    assert airplane.initial_landing_point == None
    assert airplane.waiting_point == None
    assert airplane.zero_point == None
    assert airplane.speed == 100
    assert airplane.fly_to_initial_landing_point == False
    assert airplane.fly_to_runaway == False
    assert airplane.fly_to_waiting_point == False

def test_establish_init_airplane_coordinates():
    coordinates_dict = Airplane.establish_init_airplane_coordinates()
    assert "x" in coordinates_dict
    assert "y" in coordinates_dict
    assert "z" in coordinates_dict
    assert isinstance(coordinates_dict["x"], int)
    assert isinstance(coordinates_dict["y"], int)
    assert isinstance(coordinates_dict["z"], int)
    assert -5000 <= coordinates_dict["x"] <= 5000
    assert -5000 <= coordinates_dict["y"] <= 5000
    assert 2000 <= coordinates_dict["z"] <= 5000

def test_set_points(init_airplane_obj):
    airplane = init_airplane_obj
    points = {"body": "NW",
              "init_point_coordinates": (-2000, 450, 2000),
              "waiting_point_coordinates": (-3500, 1000, 2350),
              "zero_point_coordinates": (0, 450, 0)}
    airplane.set_points(points)
    assert airplane.quarter == "NW"
    assert airplane.initial_landing_point == (-2000, 450, 2000)
    assert airplane.waiting_point == (-3500, 1000, 2350)
    assert airplane.zero_point == (0, 450, 0)

def test_fuel_consumption(init_airplane_obj):
    airplane = init_airplane_obj
    date_of_appearance_for_test = datetime.datetime.now() - datetime.timedelta(hours = 4)
    airplane.date_of_appearance = date_of_appearance_for_test
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.now.return_value = date_of_appearance_for_test + datetime.timedelta(hours = 3, seconds = 1)
        assert airplane.fuel_consumption() == False
        new_date_of_appearance = datetime.datetime.now() - datetime.timedelta(hours = 2)
        airplane.date_of_appearance = new_date_of_appearance
        assert airplane.fuel_consumption() == True

def test_avoid_collision(init_airplane_obj):
    airplane = init_airplane_obj
    airplane.avoid_collision(50)
    assert airplane.x == -4950
    assert airplane.y == 3550
    assert airplane.z == 4410

def test_direct_to_initial_landing_point_than_to_waiting_point(mocker, init_airplane_obj):
    airplane = init_airplane_obj
    mock_client_socket = mocker.Mock()
    mock_client = airplane.client
    mocker.patch.object(airplane, "count_distance_and_send_airplane_coordinates", return_value = 50)
    mock_client.read_message_from_server.return_value = {
        "message": "test_message",
        "body": "Waiting point"
    }
    airplane.direct_to_initial_landing_point(mock_client_socket)
    mock_client.send_message_to_server.assert_called_once_with(
        mock_client_socket,
        mock_client.communication_utils.reaching_the_target_message("Initial landing point")
    )
    mock_client.read_message_from_server.assert_called_once_with(mock_client_socket)
    assert airplane.fly_to_initial_landing_point == False
    assert airplane.fly_to_waiting_point == True
    assert airplane.fly_to_runaway == False
    assert airplane.speed == 100

def test_direct_to_initial_landing_point_than_to_zero_point(mocker, init_airplane_obj):
    airplane = init_airplane_obj
    mock_client_socket = mocker.Mock()
    mock_client = airplane.client
    mocker.patch.object(airplane, "count_distance_and_send_airplane_coordinates", return_value = 50)
    mock_client.read_message_from_server.return_value = {
        "message": "test_message",
        "body": "Zero point"
    }
    airplane.direct_to_initial_landing_point(mock_client_socket)
    mock_client.send_message_to_server.assert_called_once_with(
        mock_client_socket,
        mock_client.communication_utils.reaching_the_target_message("Initial landing point")
    )
    mock_client.read_message_from_server.assert_called_once_with(mock_client_socket)
    assert airplane.fly_to_initial_landing_point == False
    assert airplane.fly_to_waiting_point == False
    assert airplane.fly_to_runaway == True
    assert airplane.speed == 75

def test_direct_to_waiting_point(mocker, init_airplane_obj):
    airplane = init_airplane_obj
    mock_client_socket = mocker.Mock()
    mocker.patch.object(airplane, "count_distance_and_send_airplane_coordinates", return_value = 50)
    airplane.direct_to_waiting_point(mock_client_socket)
    assert airplane.fly_to_initial_landing_point == True
    assert airplane.fly_to_waiting_point == False

def test_direct_to_runaway(mocker, init_airplane_obj):
    airplane = init_airplane_obj
    mock_client_socket = mocker.Mock()
    mocker.patch.object(airplane, "count_distance_and_send_airplane_coordinates", return_value = 30)
    airplane.direct_to_runaway(mock_client_socket)
    airplane.client.send_message_to_server.assert_called_once_with(
        mock_client_socket, airplane.client.communication_utils.successfully_landing_message()
    )
    assert airplane.client.is_running == False

def test_parse_airplane_obj_to_json(init_airplane_obj):
    airplane = init_airplane_obj
    points = {"body": "NW",
              "init_point_coordinates": (-2000, 450, 2000),
              "waiting_point_coordinates": (-3500, 1000, 2350),
              "zero_point_coordinates": (0, 450, 0)}
    airplane.id = 1
    airplane.set_points(points)
    airplane_json = airplane.parse_airplane_obj_to_json()
    assert airplane_json == {
            f"Airplane_1": {
                "coordinates": [-5000, 3500, 4400],
                "quarter": "NW",
                "initial_landing_point": (-2000, 450, 2000),
                "waiting_point": (-3500, 1000, 2350),
                "zero_point": (0, 450, 0),
            }
        }
