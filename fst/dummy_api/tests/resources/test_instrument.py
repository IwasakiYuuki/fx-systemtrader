import pytest
import json
from jsonschema import validate

output_data_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "instruments": {
            "type": "array",
            "properties": {
                "instrument": {
                    "type": "string",
                },
                "displayName": {
                    "type": "string",
                },
                "pip": {
                    "type": "number",
                },
                "maxTradeUnits": {
                    "type": "number",
                },
                "precision": {
                    "type": "number",
                },
                "maxTrailingStop": {
                    "type": "number",
                },
                "minTrailingStop": {
                    "type": "number",
                },
                "marginRate": {
                    "type": "number",
                },
                "halted": {
                    "type": "boolean",
                },
            },
            "required": ["instrument"]
        },
    },
    "required": ["instruments"]
}


class TestInsturment(object):
    """description"""
    def test_get(self, client):
        """docstring for test_get"""
        # Send GET request to endpoint without a required argument, accountId.
        responce = client.get('/instruments')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With a required argument.
        responce = client.get('/instruments?accountId=12345')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)

    def test_get_accountId(self, client):
        """docstring for test_get_accountId"""
        # Send GET request with a wrong accountId.
        # The status code should be 404, Not Found.
        responce = client.get('/instruments?accountId=1000')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 404

        # With correct accoundId.
        responce = client.get('/instruments?accountId=12345')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)

    def test_get_instruments(self, client):
        """docstring for test_get_instruments"""
        # Send GET request with a wrong type instruments.
        # The status code should be 400, Bad Request.
        responce = client.get('/instruments?accountId=12345&instruments=100')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400
        
        # With a correct type argument.
        responce = client.get('/instruments?accountId=12345&instruments=USD_JPY')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)

        # With correct type multiple arguments.
        responce = client.get('/instruments?accountId=12345&instruments=USD_JPY%2CEUR_USD')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)
