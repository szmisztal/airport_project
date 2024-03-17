import pytest
from flask_REST_API import app, API, start_airport, close_airport, pause_airport, restore_airport, uptime, airplanes, \
    collisions, successful_landings, airplanes_in_the_air, airplane_detail


@pytest.fixture
def init_api_object():
    api = API()
    return api

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_init_API(init_api_object):
    api = init_api_object
    assert api.is_running == False
    assert api.logger is not None
    assert api.connection is not None
    assert api.db_utils is not None
    assert api.process is None



