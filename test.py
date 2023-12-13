from itertools import product
from airport import Airport
from airplane import Airplane
from connection_pool import ConnectionPool

conn = ConnectionPool(10, 100)
print(conn.connections_list)
