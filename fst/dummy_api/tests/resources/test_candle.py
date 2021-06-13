import pytest
import json
from jsonschema import validate


output_data_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "instrument": {
            "type": "string"
        },
        "granularity": {
            "type": "string"
        },
        "candles": {
            "type": "array",
            "properties": {
                "time": {
                    "type": "string",
                },
                "openBid": {
                    "type": "string",
                    "format": "date-time",
                },
                "openAsk": {
                    "type": "number",
                },
                "highBid": {
                    "type": "number",
                },
                "highAsk": {
                    "type": "number",
                },
                "lowBid": {
                    "type": "number",
                },
                "lowAsk": {
                    "type": "number",
                },
                "closeBid": {
                    "type": "number",
                },
                "closeAsk": {
                    "type": "number",
                },
                "openMid": {
                    "type": "number",
                },
                "highMid": {
                    "type": "number",
                },
                "lowMid": {
                    "type": "number",
                },
                "closeMid": {
                    "type": "number",
                },
                "volume": {
                    "type": "number",
                },
                "complete": {
                    "type": "boolean",
                },
            },
            "required": [
                "time",
                "volume",
                "complete",
            ]
        },
    },
    "required": ["candles"]
}


class TestCandle(object):
    """description"""
    def test_get(self, client):
        """docstring for test_get"""
        # Send GET request to endpoint without a required argument, instrument.
        # The status code should be 400, Bad Request. (RequiredParams)
        responce = client.get('/candles')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With a required argument.
        responce = client.get('/candles?instrument=USD_JPY')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)
        
    def test_get_instrument(self, client):
        """docstring for test_get_instrument"""
        # Send GET request with a wrong argument, instrument.
        # The status code should be 400, Bad Request. (InvalidInstrumentPair)
        responce = client.get('/candles?instrument=1000')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With correct instrument (string).
        responce = client.get('/candles?instrument=USD_JPY')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)

    def test_get_granularity(self, client):
        """docstring for test_get_granularity"""
        # Send GET request with a wrong argument, granularity.
        # The status code should be 400, Bad Request. (InvalidParams)
        responce = client.get('/candles?instrument=USD_JPY&granularity=hogehoge')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 400

        # With correct granularity (string, and it should be specified format).
        responce = client.get('/candles?instrument=USD_JPY&granularity=S10')
        assert responce.content_type == 'application/json'
        assert responce.status_code == 200
        json_data = json.loads(responce.data.decode())
        validate(json_data, schema=output_data_schema)
