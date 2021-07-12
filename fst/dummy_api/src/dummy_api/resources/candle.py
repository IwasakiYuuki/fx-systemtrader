import random
import datetime
from flask import jsonify, make_response
from flask_restful import Resource, reqparse, inputs
from dummy_api.common import exceptions


instrument_list = [
    'USD_JPY',
    'EUR_USD',
    'CAD_JPY',
    'GBP_AUD',
    'AUD_CAD',
]

parser = reqparse.RequestParser()
parser.add_argument(
    'instrument',
    dest='instrument',
)
parser.add_argument(
    'granularity',
    dest='granularity',
    default="S5",
)
parser.add_argument(
    'count',
    dest='count',
    default=500,
)
parser.add_argument(
    'start',
    dest='start',
)
parser.add_argument(
    'end',
    dest='end',
)
parser.add_argument(
    'candleFormat',
    dest='candleFormat',
    default="bidask",
)
parser.add_argument(
    'includeFirst',
    dest='includeFirst',
    default="True",
)
parser.add_argument(
    'dailyAlignment',
    dest='dailyAlignment',
    default=22,
)
parser.add_argument(
    'alignmentTimezone',
    dest='alignmentTimezone',
    default="America/New_York",
)
parser.add_argument(
    'weeklyAlignment',
    dest='weeklyAlignment',
    default="Friday",
)


class Candle(Resource):
    def get(self):
        """docstring for get"""
        args = parser.parse_args()

        try:
            instrument = args.instrument
            if instrument is None:
                raise exceptions.RequiredParams()
            if instrument not in instrument_list:
                raise exceptions.InvalidInstrumentPair()

            granularity = args.granularity
            if granularity is not None and granularity not in [
                "S5",
                "S10",
                "S15",
                "S30",
                "M1",
                "M2",
                "M3",
                "M5",
                "M15",
                "M30",
                "H1",
                "H2",
                "H3",
                "H4",
                "H6",
                "H8",
                "H12",
                "D",
                "W",
                    "M"]:
                raise exceptions.InvalidParams(arg_name="granularity")

            count = int(args.count)
            if not 0 <= count <= 5000:
                raise exceptions.InvalidParams(arg_name="count")

            start = args.start
            if start:
                start = datetime.datetime.fromisoformat(
                    start.replace("Z", "+00:00"))

            end = args.end
            if end:
                end = datetime.datetime.fromisoformat(
                    end.replace("Z", "+00:00"))

            candle_format = args.candleFormat
            if candle_format not in ["midpoint", "bidask"]:
                raise exceptions.InvalidParams(arg_name="candleFormat")

            include_first = args.includeFirst
            if not (include_first == "True" or include_first == "False"):
                raise exceptions.InvalidParams(arg_name="includeFirst")
            if include_first == "True":
                include_first = True
            elif include_first == "False":
                include_first = False

            daily_alignment = int(args.dailyAlignment)
            if not 0 <= daily_alignment <= 23:
                raise exceptions.InvalidParams(arg_name="dailyAlignment")

            alignment_timezone = args.alignmentTimezone

            weekly_alignment = args.weeklyAlignment
            if weekly_alignment not in ["Monday",
                                        "Tuesday",
                                        "Wednesday",
                                        "Thursday",
                                        "Friday",
                                        "Saturday",
                                        "Sunday"]:
                raise exceptions.InvalidParams(arg_name="weeklyAlignment")

        except (ValueError, TypeError):
            raise exceptions.InvalidParams(arg_name="unknow")

        def granu_to_timedelta(granu):
            if len(granu) == 1:
                unit, num = granu, None
            else:
                unit, num = granu[0], int(granu[1:])

            if num:
                arg = {{"S": "seconds",
                        "M": "minutes",
                        "H": "hours"}[unit]: num}
            else:
                arg = {"days": {"D": 1,
                                "W": 7,
                                "M": 30, }[unit]}

            return datetime.timedelta(**arg)

        def gen_candle(time, candleformat):
            candle = dict()
            candle["time"] = time.isoformat() + "Z"
            if candleformat == "midpoint":
                candle.update({
                    "openMid": random.uniform(1.0, 2.0),
                    "highMid": random.uniform(1.0, 2.0),
                    "lowMid": random.uniform(1.0, 2.0),
                    "closeMid": random.uniform(1.0, 2.0),
                })
            elif candleformat == "bidask":
                candle.update({
                    "openBid": random.uniform(1.0, 2.0),
                    "openAsk": random.uniform(1.0, 2.0),
                    "highBid": random.uniform(1.0, 2.0),
                    "highAsk": random.uniform(1.0, 2.0),
                    "lowBid": random.uniform(1.0, 2.0),
                    "lowAsk": random.uniform(1.0, 2.0),
                    "closeBid": random.uniform(1.0, 2.0),
                    "closeAsk": random.uniform(1.0, 2.0),
                })
            candle["volume"] = random.randrange(1, 10)
            candle["complete"] = True
            return candle

        try:
            candles = []
            delta = granu_to_timedelta(granularity)
            if start and end:
                current = start
                while current < end:
                    candles.append(gen_candle(current, candle_format))
                    current += delta

            else:
                if start:
                    end = datetime.datetime.now(datetime.timezone.utc)
                    current = start
                    for i in range(count):
                        candles.append(gen_candle(current, candle_format))
                        current += delta
                        if current > end:
                            break

                else:
                    end = datetime.datetime.now(datetime.timezone.utc)
                    current = end
                    for i in range(count):
                        candles.append(gen_candle(current, candle_format))
                        current -= delta

            response = make_response(jsonify({
                "instrument": instrument,
                "granularity": granularity,
                "candles": candles,
            }), 200)

        except BaseException:
            raise exceptions.InternalServerError()

        return response
