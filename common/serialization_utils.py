import json
from common.config_variables import encode_format


class SerializeUtils:
    """
    Utility class for serializing and deserializing data to and from JSON format.
    """

    def serialize_to_json(self, dict_data):
        """
        Serialize a dictionary to JSON format.

        Parameters:
        - dict_data (dict): The dictionary to be serialized.

        Returns:
        - bytes: The JSON-encoded data.
        """
        return json.dumps(dict_data).encode(encode_format)

    def deserialize_json(self, dict_data):
        """
        Deserialize JSON data to a dictionary.

        Parameters:
        - dict_data (bytes): The JSON-encoded data.

        Returns:
        - dict: The deserialized dictionary.
        """
        return json.loads(dict_data)
