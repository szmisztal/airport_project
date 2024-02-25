import os
import pytest
from server_side.connection_pool import Connection, ConnectionPool


@pytest.fixture
def init_connection_obj():
    db_file = f"{os.path.dirname(os.path.realpath(__file__))}/test_app_db.db"
    connection = Connection(db_file)
    connection.db_file = db_file
    return connection

@pytest.fixture
def init_pool():
    pool = ConnectionPool(10, 100)
    return pool

def test_init_connection_obj(init_connection_obj):
    connection = init_connection_obj
    assert connection.in_use == False

def test_init_pool(init_pool):
    pool = init_pool
    assert len(pool.connections_list) == 10
    assert len(pool.connections_in_use_list) == 0
    assert pool.min_number_of_connections == 10
    assert pool.max_number_of_connections == 100

def test_get_connection(init_pool):
    pool = init_pool
    pool.get_connection()
    assert len(pool.connections_list) == 9
    assert len(pool.connections_in_use_list) == 1
    for _ in range(99):
        pool.get_connection()
    assert pool.get_connection() == False

def test_release_connection(init_pool):
    pool = init_pool
    conn = pool.get_connection()
    assert len(pool.connections_in_use_list) == 1
    assert conn.in_use == True
    pool.release_connection(conn)
    assert len(pool.connections_in_use_list) == 0
    assert conn.in_use == False

def test_destroy_unused_connections(init_pool):
    pool = init_pool
    for _ in range(20):
        conn = pool.get_connection()
        pool.connections_list.append(conn)
    assert len(pool.connections_list) == 20
    pool.destroy_unused_connections()
    assert len(pool.connections_list) == 10

def test_keep_connections_at_the_starting_level(init_pool):
    pool = init_pool
    for _ in range(2):
        pool.get_connection()
    assert len(pool.connections_list) == 8
    pool.keep_connections_at_the_starting_level()
    assert len(pool.connections_list) == 10
