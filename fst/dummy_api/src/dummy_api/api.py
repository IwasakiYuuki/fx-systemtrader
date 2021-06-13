"""
File: api-server.py
Author: Yuuki Iwasaki
Email: 2445yuuki@gmail.com
Github: https://github.com/IwasakiYuuki
Description: 
A dummy of OANDA API. This API server sends random values related to fx.
"""
from flask import Flask, request, json, jsonify, Blueprint
from flask_restful import reqparse, abort, Resource, Api
from dummy_api.resources.instrument import Instrument
from dummy_api.resources.price import Price
from dummy_api.resources.candle import Candle
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
api = Api(app)

api.add_resource(Instrument, '/instruments')
api.add_resource(Price, '/prices')
api.add_resource(Candle, '/candles')

@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    if isinstance(e, HTTPException):
        response = e.get_response()
        # replace the body with JSON
        #response.data = json.dumps({
        #    "code": e.code,
        #    "message": e.description,
        #    "moreInfo": getattr(e, 'moreInfo', None),
        #})
        return jsonify(
            code=e.code,
            message=e.description,
            moreInfo=getattr(e, 'moreInfo', None),
        ), e.code
        #response.content_type = "application/json"
        #return response, e.code
    
    return jsonify(
        code=500,
        message="{}:{}".format(e.__class__.__name__,str(e)),
        moreInfo=getattr(e, 'moreInfo', None),
    ), 500
    
def main():
    app.run(debug=False, host="0.0.0.0", port=80)

if __name__ == '__main__':
    main()
