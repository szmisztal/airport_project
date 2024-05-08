import socket as s
import os


"""
HOST: str
    The IP address of the server_side to connect to.

PORT: int
    The port number on the server_side to connect to.

BUFFER: int
    The size of the buffer used for sending and receiving data over sockets.

encode_format: str
    The encoding format used for encoding and decoding strings.

INTERNET_ADDRESS_FAMILY: int
    The address family used for the socket connection.

SOCKET_TYPE: int
    The type of socket used for the connection.

db_file: str
    The filename of the SQLite database file used for storing airport-related data.
"""

HOST = "127.0.0.1"
PORT = 65432
BUFFER = 1024
encode_format = "UTF-8"
INTERNET_ADDRESS_FAMILY = s.AF_INET
SOCKET_TYPE = s.SOCK_STREAM
db_file = f"{os.path.dirname(os.path.realpath(__file__))}/app_db.db"


