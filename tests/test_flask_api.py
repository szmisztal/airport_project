import os
import subprocess
import pytest
from flask_REST_API import app, API, start_airport, close_airport, pause_airport, restore_airport, uptime, airplanes, \
    collisions, successful_landings, airplanes_in_the_air, airplane_detail


@pytest.fixture
def init_api_object():
    api = API()
    return api

def test_init_API(init_api_object):
    api = init_api_object
    assert api.logger is not None
    assert api.connection is not None
    assert api.db_utils is not None
    assert api.process is None

def test_server_start(mocker, init_api_object):
    api = init_api_object
    mock_popen = mocker.patch("subprocess.Popen")
    mock_process = mocker.MagicMock()
    mock_process.pid = 12345
    mock_popen.return_value = mock_process
    process = api.server_start()
    assert api.process is not None
    assert process.pid == 12345
    mock_popen.assert_called_with(["python", f"{os.getcwd()}/server_side/server.py"], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True)

def test_server_close(mocker, init_api_object):
    api = init_api_object
    mock_process = mocker.MagicMock()
    api.process = mock_process
    response = api.server_close()
    mock_process.terminate.assert_called_once()
    mock_process.wait.assert_called_once()
    assert response == {"message": "Server stopped"}

def test_server_pause(mocker, init_api_object):
    api = init_api_object
    mock_open = mocker.patch('builtins.open', mocker.mock_open())
    response = api.server_pause()
    mock_open.assert_called_once_with(f"{os.getcwd()}\\server_side\\flag_file.txt", "w")
    assert response == {"server status": "paused"}

def test_server_resume_when_file_exists(mocker, init_api_object):
    api = init_api_object
    mocker.patch("os.path.isfile", return_value = True)
    mock_remove = mocker.patch("os.remove")
    response = api.server_resume()
    mock_remove.assert_called_once_with(f"{os.getcwd()}\\server_side\\flag_file.txt")
    assert response == {"server status": "resumed"}

def test_server_resume_when_file_does_not_exist(mocker, init_api_object):
    api = init_api_object
    mocker.patch("os.path.isfile", return_value = False)
    response = api.server_resume()
    assert response is None

def test_number_of_airplanes(mocker, init_api_object):
    api = init_api_object
    mocker.patch("flask_REST_API.DatabaseUtils.get_all_airplanes_number_per_period", return_value = 5)
    result = api.number_of_airplanes()
    assert result == 5

def test_airplanes_by_status(mocker, init_api_object):
    api = init_api_object
    mock_airplanes = [{"id": 1, "status": "Test_status"}]
    mocker.patch("flask_REST_API.DatabaseUtils.get_airplanes_with_specified_status_per_period", return_value = mock_airplanes)
    result = api.airplanes_by_status("Test_status")
    assert result == mock_airplanes

def test_single_airplane_details(mocker, init_api_object):
    api = init_api_object
    mock_details = {"id": 1, "status": "Test_status"}
    mocker.patch("flask_REST_API.DatabaseUtils.get_single_airplane_details", return_value = mock_details)
    result = api.single_airplane_details(1)
    assert result == mock_details

