import requests
import datetime
import json
from google.cloud import storage


def get_rates(request):
    endpoint = "http://192.168.10.10:80/candles"
    # endpoint = "http://api-fxtrade.oanda.com/v1/candles"

    instrument = "USD_JPY"
    granularity = "M5"
    include_first = False
    end = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start = end - datetime.timedelta(days=1)

    def dt_to_str(dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    params = {
        "instrument": instrument,
        "granularity": granularity,
        "start": dt_to_str(start),
        "end": dt_to_str(end),
        "includeFirst": include_first,
    }

    response = requests.get(
        endpoint,
        params=params,
    )
    print("Receive response")

    if response.status_code != 200:
        print("Responsed status code is not 200.")
        print(response.status_code)
        return "hoge"
    print("Status code is 200.")

    if response.headers["Content-Type"] != "application/json":
        print("Responsed content is not json format.")
        print(response.headers["Content-Type"])
        return "huga"
    print("Response header is application/json type")

    data = response.json()
    json_data = json.dumps(data, ensure_ascii=False, indent=2)
    print("Complete dump to json data")

    upload_blob(
        "fx-systemtrader-dev-datalake",
        json_data,
        "rates/{}/{}.json".format(instrument, start.strftime("%Y/%m/%d"))
    )
    print("Complete make object into GCS")

    return "Successful completion"


def upload_blob(bucket_name, data, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(data, content_type='application/json')
