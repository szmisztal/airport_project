import pytest
from data_utils import SerializeUtils, DatabaseUtils


@pytest.fixture
def init_serialize_utils_obj():
    serialize_utils = SerializeUtils()
    return serialize_utils

def test_serialize_to_json(init_serialize_utils_obj):
    utils = init_serialize_utils_obj
    data = {"test_key": "test_value",
            "test_key_2": ["test_value_2", "test_value_3"]}
    serialized_data = utils.serialize_to_json(data)
    assert serialized_data == b'{"test_key": "test_value", "test_key_2": ["test_value_2", "test_value_3"]}'

def test_deserialize_json(init_serialize_utils_obj):
    utils = init_serialize_utils_obj
    serialized_data = b'{"test_key": "test_value", "test_key_2": ["test_value_2", "test_value_3"]}'
    deserialized_data = utils.deserialize_json(serialized_data)
    assert deserialized_data == {"test_key": "test_value",
            "test_key_2": ["test_value_2", "test_value_3"]}


@pytest.fixture
def init_database_utils_obj():
    utils = DatabaseUtils()
    return utils

@pytest.fixture
def mock_connection(mocker):
    conn = mocker.Mock()
    return conn

def test_create_server_periods_table(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mock_create_tables = mocker.patch.object(utils, "create_server_periods_table")
    utils.create_server_periods_table(mock_connection)
    mock_create_tables.assert_called_once_with(mock_connection)

def test_create_connections_table(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mock_create_tables = mocker.patch.object(utils, "create_connections_table")
    utils.create_connections_table(mock_connection)
    mock_create_tables.assert_called_once_with(mock_connection)

def test_create_db_tables(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mock_create_tables = mocker.patch.object(utils, "create_db_tables")
    utils.create_db_tables(mock_connection)
    mock_create_tables.assert_called_once_with(mock_connection)

def test_add_new_server_period(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mocker.patch.object(utils, "execute_sql_query")
    utils.add_new_server_period(mock_connection)
    expected_query = "INSERT INTO server_periods DEFAULT VALUES"
    utils.execute_sql_query.assert_called_once_with(mock_connection, expected_query)

def test_add_new_connection_to_db(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    airplane_id = 123
    mocker.patch.object(utils, "get_period_id", return_value = 1)
    mocker.patch.object(utils, "execute_sql_query")
    utils.add_new_connection_to_db(mock_connection, airplane_id)
    utils.get_period_id.assert_called_once_with(mock_connection)
    expected_query = "INSERT INTO connections (period_id, airplane_id) VALUES (?, ?)"
    expected_args = (1, airplane_id)
    utils.execute_sql_query.assert_called_once_with(mock_connection, expected_query, expected_args)

def test_update_connection_status(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    status = "TEST STATUS"
    airplane_id = 123
    mocker.patch.object(utils, "get_period_id", return_value = 1)
    mocker.patch.object(utils, "execute_sql_query")
    utils.update_connection_status(mock_connection, status, airplane_id)
    utils.get_period_id.assert_called_once_with(mock_connection)
    expected_query = "UPDATE connections SET status = ? WHERE connection_id = (SELECT connection_id FROM connections WHERE period_id = ? AND airplane_id = ?)"
    expected_args = (status, 1, airplane_id)
    utils.execute_sql_query.assert_called_once_with(mock_connection, expected_query, expected_args)

def test_update_period_end(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mocker.patch.object(utils, "get_period_id", return_value = 1)
    mocker.patch.object(utils, "execute_sql_query")
    utils.update_period_end(mock_connection)
    utils.get_period_id.assert_called_once_with(mock_connection)
    expected_query = "UPDATE server_periods SET period_end = CURRENT_TIMESTAMP WHERE period_id = ?"
    expected_args = (1, )
    utils.execute_sql_query.assert_called_once_with(mock_connection, expected_query, expected_args)

def test_get_period_id(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mock_get_period = mocker.patch.object(utils, "get_period_id")
    mock_get_period.return_value = 1
    period_id = utils.get_period_id(mock_connection)
    assert period_id == 1

def test_get_all_airplanes_number_per_period(mocker, init_database_utils_obj, mock_connection):
    utils = init_database_utils_obj
    mocker.patch.object(utils, "get_period_id", return_value = 1)
    mocker.patch.object(utils, "execute_sql_query")
    mock_get_all_airplanes = mocker.patch.object(utils, "get_all_airplanes_number_per_period")
    mock_get_all_airplanes.return_value = 10
    all_airplanes = utils.get_all_airplanes_number_per_period(mock_connection)
    assert all_airplanes == 10
