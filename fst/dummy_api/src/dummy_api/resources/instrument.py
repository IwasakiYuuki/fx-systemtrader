from flask_restful import Resource, reqparse
from flask import jsonify, make_response
from dummy_api.common import exceptions


instrument_data = {
    'USD_JPY': {
        'instrument': 'USD_JPY',
        'pip': 0.0001,
        'maxTradeUnits': 10000000,
        'precision': 0.001,
        'maxTrailingStop': 1000,
        'minTrailingStop': 1,
        'marginRate': 0.04,
        'halted': True,
    },
    'EUR_USD': {
        'instrument': 'EUR_USD',
        'pip': 0.0001,
        'maxTradeUnits': 10000000,
        'precision': 0.001,
        'maxTrailingStop': 1000,
        'minTrailingStop': 1,
        'marginRate': 0.04,
        'halted': True,
    },
    'CAD_JPY': {
        'instrument': 'CAD_JPY',
        'pip': 0.0001,
        'maxTradeUnits': 10000000,
        'precision': 0.001,
        'maxTrailingStop': 1000,
        'minTrailingStop': 1,
        'marginRate': 0.04,
        'halted': True,
    },
    'GBP_AUD': {
        'instrument': 'GBP_AUD',
        'pip': 0.0001,
        'maxTradeUnits': 10000000,
        'precision': 0.001,
        'maxTrailingStop': 1000,
        'minTrailingStop': 1,
        'marginRate': 0.04,
        'halted': True,
    },
    'AUD_CAD': {
        'instrument': 'AUD_CAD',
        'pip': 0.0001,
        'maxTradeUnits': 10000000,
        'precision': 0.001,
        'maxTrailingStop': 1000,
        'minTrailingStop': 1,
        'marginRate': 0.04,
        'halted': True,
    },
}

available_accountId = [
    12345,
    67890,
    11111,
    22222,
]

parser = reqparse.RequestParser()
parser.add_argument(
    'accountId',
    dest='accountId',
)
parser.add_argument(
    'fields',
    dest='fields',
)
parser.add_argument(
    'instruments',
    dest='instruments',
)


class Instrument(Resource):
    def get(self):
        """Get the list of instruments."""
        args = parser.parse_args()
        if args.accountId is  None:
            raise exceptions.RequiredParams()
        try:
            accountId = int(args.accountId)
            if accountId not in available_accountId:
                raise exceptions.AccountNotFound()

            if args.fields:
                fields = args.fields.split(",")
            else:
                fields = None

            instruments = []
            if args.instruments:
                for instrument in args.instruments.split(","):
                    if instrument in instrument_data:
                        instruments.append(instrument_data[instrument])
                    else:
                        raise exceptions.InvalidInstrumentPair()
            else:
                for _, instrument in instrument_data.items():
                    instruments.append(instrument)

        except ValueError:
            raise exceptions.InvalidParams()

        try:
            response = dict()
            response["instruments"] = []
            
            displayName = "testuser"

            for instrument in instruments:
                data = dict()
                data["instrument"] = instrument["instrument"]
                if fields:
                    if "displayName" in fileds:
                        data["displayName"] = displayName
                    for field in fields:
                        if field in instrument:
                            data[field] = instrument[field]
                else:
                    data["displayName"] = displayName
                    data["pip"] = instrument["pip"]
                    data["maxTradeUnits"] = instrument["maxTradeUnits"]
                response["instruments"].append(data)
        except:
            raise exceptions.InternalServerError()

        return make_response(jsonify(response), 200)
