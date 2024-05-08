import os
import pytest
import socket as s
from server_side.server import Server, ClientHandler
from server_side.database_managment import SerializeUtils


@pytest.fixture
def init_server(mock_connection_pool):
    connection_pool = mock_connection_pool
    server = Server(connection_pool)
    return server

@pytest.fixture
def mock_connection_pool(mocker):
    connection_pool = mocker.Mock()
    return connection_pool

@pytest.fixture
def mock_socket(mocker):
    socket = mocker.Mock()
    return socket

@pytest.fixture
def init_client_handler(init_server, mock_socket, mocker, mock_connection_pool):
    server = init_server
    connection_pool = mock_connection_pool
    client_handler = ClientHandler(server, mock_socket, ("127.0.0.1", 65433), 10)
    client_handler.connection = mocker.Mock()
    return client_handler

def test_client_handler_init(init_client_handler):
    client_handler = init_client_handler
    assert client_handler.address == ("127.0.0.1", 65433)
    assert client_handler.thread_id == 10
    assert client_handler.BUFFER == 1024
    assert client_handler.is_running == True
    assert client_handler.airplane_object == None
    assert client_handler.airplane_key == f"Airplane_10"

def test_send_message_to_client(init_client_handler, mock_socket, mocker):
    client_handler = init_client_handler
    mocked_socket = mock_socket
    serialize_utils = SerializeUtils()
    data = {"message": "Test message", "body": "Test body"}
    b_data = b'{"message": "Test message", "body": "Test body"}'
    mocker.patch.object(serialize_utils, "serialize_to_json")
    client_handler.send_message_to_client(data)
    mocked_socket.sendall.assert_called_once_with(b_data)

def test_read_message_from_client(init_client_handler, mock_socket, mocker):
    client_handler = init_client_handler
    mocked_socket = mock_socket
    serialize_utils = SerializeUtils()
    mocked_socket.recv.return_value = b'{"message": "Test message", "body": "Test body"}'
    expected_message = {"message": "Test message", "body": "Test body"}
    mocker.patch.object(serialize_utils, "deserialize_json", return_value = expected_message)
    received_message = client_handler.read_message_from_client(mocked_socket)
    assert received_message == expected_message
    mocked_socket.recv.assert_called_once_with(client_handler.BUFFER)

def test_update_airplane_coordinates(init_client_handler, mocker):
    client_handler = init_client_handler
    client_handler.airplane_object = {
        client_handler.airplane_key: {
            "coordinates": [-5000, 2000, 3000]
        }
    }
    mocked_possible_collisions = mocker.Mock()
    client_handler.check_possible_collisions = mocked_possible_collisions
    updated_coordinates = {"body": {"x": -4500, "y": 2500, "z": 2600}}
    client_handler.update_airplane_coordinates(updated_coordinates)
    mocked_possible_collisions.assert_called_once()
    assert client_handler.airplane_object[client_handler.airplane_key]["coordinates"] == [
        updated_coordinates["body"]["x"],
        updated_coordinates["body"]["y"],
        updated_coordinates["body"]["z"]
    ]

def test_server_init(init_server):
    server = init_server
    assert server.HOST == "127.0.0.1"
    assert server.PORT == 65432
    assert server.INTERNET_ADDRESS_FAMILY == s.AF_INET
    assert server.SOCKET_TYPE == s.SOCK_STREAM
    assert server.is_running == True
    assert server.version == "1.2.3"
    assert len(server.clients_list) == 0

def test_check_file_flag_exsits(mocker, init_server):
    server = init_server
    mock_os_path_is_file = mocker.patch.object(os.path, "isfile")
    mock_os_path_is_file.return_value = True
    check_file_flag_not_exists = server.check_file_flag_exists()
    assert check_file_flag_not_exists == True

def test_check_file_flag_not_exsits(init_server, mocker):
    server = init_server
    mock_os_path_is_file = mocker.patch.object(os.path, "isfile")
    mock_os_path_is_file.return_value = False
    check_file_flag_not_exists = server.check_file_flag_exists()
    assert check_file_flag_not_exists == False
