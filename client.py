import socket as s
from variables import HOST, PORT, INTERNET_ADDRESS_FAMILY, SOCKET_TYPE, BUFFER, encode_format
from data_utils import DataUtils
from airplane import Airplane
from communication_utils import ClientProtocols


class Client:
    def __init__(self):
        self.HOST = HOST
        self.PORT = PORT
        self.INTERNET_ADDRESS_FAMILY = INTERNET_ADDRESS_FAMILY
        self.SOCKET_TYPE = SOCKET_TYPE
        self.BUFFER = BUFFER
        self.encode_format = encode_format
        self.data_utils = DataUtils()
        self.is_running = True
        self.communication_utils = ClientProtocols()
        self.airplane = Airplane(Airplane.establish_init_airplane_coordinates())

    def read_server_response(self, dict_data):
        deserialized_data = self.data_utils.deserialize_json(dict_data)
        return f">>> {deserialized_data['message']}: {deserialized_data['body']}."

    def start(self):
        with s.socket(INTERNET_ADDRESS_FAMILY, SOCKET_TYPE) as client_socket:
            print("CLIENT`S UP...")
            client_socket.connect((HOST, PORT))
            server_response_json = client_socket.recv(self.BUFFER)
            server_response = self.read_server_response(server_response_json)
            print(server_response)
            self.airplane.id = server_response[int("id")]
            client_socket.sendall(self.data_utils.serialize_to_json(client_request))
            while self.is_running:
                server_response_json = client_socket.recv(self.BUFFER)
                server_response = self.read_server_response(server_response_json)
                    
    def stop(self, client_socket):
        print("CLIENT`S OUT...")
        self.is_running = False
        client_socket.close()


if __name__ == "__main__":
    client = Client()
    client.start()
