import pytest
from server_side.server_messages import CommunicationUtils


@pytest.fixture
def init_communication_utils_obj():
    communication_utils = CommunicationUtils()
    return communication_utils

@pytest.mark.parametrize("message, body, kwargs, result", [
    ("test_message", "test_body", None, {"message": "test_message", "body": "test_body", "kwargs": None}),
    (None, "test_body", "test_kwargs", {"message": None, "body": "test_body", "kwargs": "test_kwargs"}),
    ("test_message", None, "test_kwargs", {"message": "test_message", "body": None, "kwargs": "test_kwargs"}),
    ("test_message", "test_body", "test_kwargs", {"message": "test_message", "body": "test_body", "kwargs": "test_kwargs"}),
    (None, None, "test_kwargs", {"message": None, "body": None, "kwargs": "test_kwargs"}),
    (None, None, None, {"message": None, "body": None, "kwargs": None})
])
def test_protocol_template(init_communication_utils_obj, message, body, kwargs, result):
    communication_utils = init_communication_utils_obj
    assert communication_utils.protocol_template(message = message, body = body, kwargs = kwargs) == result
