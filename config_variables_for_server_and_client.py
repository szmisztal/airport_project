import socket as s
import os
import logging


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


def logger_config(logger_name, log_folder, log_file_name):
    """
    Configure logger for the application.

    Args:
    - log_folder (str): Path to the log folder.
    - file_name (str): Name of the log file.

    Returns:
    logging.Logger: Configured logger object.
    """
    log_path = os.path.join(logger_name, log_folder, log_file_name)
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(logger_name)
