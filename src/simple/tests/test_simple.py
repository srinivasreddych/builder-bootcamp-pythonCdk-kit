import json

import pytest

import simple.app as app

def test_200_success():
    event = {}
    result = app.handler(event, "")
    assert isinstance(result, dict)
    assert result["statusCode"] == 200
    assert isinstance(result['body'], str)

    response = json.loads(result["body"])
    assert isinstance(response, dict)
    assert response['message'] == "hello simple world!"