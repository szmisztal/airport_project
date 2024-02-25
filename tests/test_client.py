import pytest
import socket as s
from client_side.client import Client
from client_side.airplane import Airplane
from server_side.database_and_serialization_managment import SerializeUtils


@pytest.fixture
def init_client():
    client = Client()
    return client

@pytest.fixture
def get_airplane_obj(init_client):
    coordinates = {"x": -5000, "y": 3500, "z": 4400}
    airplane = Airplane(init_client, coordinates)
    return airplane

@pytest.fixture
def mock_client_socket(mocker):
    client = mocker.Mock()
    return client

def test_client_init(init_client, get_airplane_obj):
    client = init_client
    client.airplane = get_airplane_obj
    assert client.HOST == "127.0.0.1"
    assert client.PORT == 65432
    assert client.INTERNET_ADDRESS_FAMILY == s.AF_INET
    assert client.SOCKET_TYPE == s.SOCK_STREAM
    assert client.BUFFER == 1024
    assert client.encode_format == "UTF-8"
    assert client.is_running == True
    assert client.airplane.x == -5000
    assert client.airplane.y == 3500
    assert client.airplane.z == 4400

def test_read_message_from_server(mocker, init_client, mock_client_socket):
    client = init_client
    mocked_client_socket = mock_client_socket
    serialize_utils = SerializeUtils()
    mocked_client_socket.recv.return_value = b'{"message": "Test message", "body": "Test body"}'
    expected_message = {"message": "Test message", "body": "Test body"}
    mocker.patch.object(serialize_utils, "deserialize_json", return_value = expected_message)
    received_message = client.read_message_from_server(mocked_client_socket)
    assert received_message == expected_message
    mocked_client_socket.recv.assert_called_once_with(client.BUFFER)

def test_send_message_to_server(mocker, init_client, mock_client_socket):
    client = init_client
    mocked_client_socket = mock_client_socket
    serialize_utils = SerializeUtils()
    data = {"message": "Test message", "body": "Test body"}
    b_data = b'{"message": "Test message", "body": "Test body"}'
    mocker.patch.object(serialize_utils, "serialize_to_json")
    client.send_message_to_server(mocked_client_socket, data)
    mocked_client_socket.sendall.assert_called_once_with(b_data)
