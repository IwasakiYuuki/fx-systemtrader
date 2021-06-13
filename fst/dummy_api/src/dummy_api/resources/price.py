import random
import datetime
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from dummy_api.common import exceptions


parser = reqparse.RequestParser()
parser.add_argument(
    'instruments',
    dest='instruments',
)
parser.add_argument(
    'since',
    dest='since',
)

instrument_list = [
    'USD_JPY',
    'EUR_USD',
    'CAD_JPY',
    'GBP_AUD',
    'AUD_CAD',
]

class Price(Resource):
    def get(self):
        """docstring for get"""
        args = parser.parse_args()
        if args.instruments is None:
            raise exceptions.RequiredParams()

        instruments = []
        for instrument in args.instruments.split(","):
            if instrument in instrument_list:
                instruments.append(instrument)
            else:
                raise exceptions.InvalidInstrumentPair()

        try:
            if args.since:
                since = datetime.datetime.fromisoformat(args.since.replace('Z', '+00:00'))
        except:
            raise exceptions.InvalidDatetimeFormat()

        try:
            response = dict()
            response['prices'] = []
            for instrument in instruments:
                response['prices'].append({
                    "instrument": instrument,
                    "time": datetime.datetime.utcnow().isoformat()+"Z",
                    "bid": random.uniform(1.0, 2.0),
                    "ask": random.uniform(1.0, 2.0),
                })
        except:
            raise exceptions.InternalServerError()

        return make_response(jsonify(response), 200)
