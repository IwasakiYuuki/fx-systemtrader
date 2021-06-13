import pytest
import json
from jsonschema import validate


output_data_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "prices": {
            "type": "array",
            "properties": {
                "instrument": {
                    "type": "string",
                },
                "time": {
                    "type": "string",
                    "format": "date-time",
                },
                "bid": {
                    "type": "number",
                },
                "ask": {
                    "type": "number",
                },
            },
            "required": [
                "instrument",
                "time",
                "bid",
                "ask",
            ]
        },
    },
    "required": ["prices"]
}


class TestPrice(object):
    """description"""
    def test_get(self, client):
        """docstring for test_get"""
        # Send GET request to endpoint without a required argument, instruments.
        # The status code should be 400, Bad Request. (RequiredParams)
        responce = client.get('/prices')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With a required argument.
        responce = client.get('/prices?instruments=USD_JPY')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)
        
    def test_get_instruments(self, client):
        """docstring for test_get_instruments"""
        # Send GET request with a wrong argument, instruments.
        # The status code should be 400, Bad Request. (InvalidInstrumentPair)
        responce = client.get('/prices?instruments=1000')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With correct instruments (string).
        responce = client.get('/prices?instruments=USD_JPY')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)

    def test_get_since(self, client):
        """docstring for test_get_since"""
        # Send GET request with a wrong argument, since.
        # The status code should be 400, Bad Request. (InvalidDatetimeFormat)
        responce = client.get('/prices?instruments=USD_JPY&since=1000')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With correct since (RFC3339 or UNIX datetime format).
        responce = client.get('/prices?instruments=USD_JPY&since=2014-06-19T15%3A47%3A50Z')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)
