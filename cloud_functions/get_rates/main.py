import requests
import datetime
import json
from google.cloud import storage


def get_rates(request):
    def _get_access_token():
        client = storage.Client()
        bucket = client.bucket("fx-systemtrader-dev-certifications")
        blob = bucket.get_blob("oanda_access-token-demo.txt")
        return blob.download_as_text()

    # endpoint = "http://192.168.10.10:80/candles"
    endpoint = "https://api-fxpractice.oanda.com/v3/instruments"
    # endpoint = "https://api-fxtrade.oanda.com"
    instrument = "USD_JPY"
    endpoint = "{}/{}/{}".format(endpoint, instrument, "candles")

    headers = {
        "Authorization": "Bearer {}".format(_get_access_token()),
        "Content-Type": "application/json"
    }

    granularity = "M5"
    include_first = False
    end = datetime.datetime.utcnow().replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    start = end - datetime.timedelta(days=1)

    def dt_to_str(dt):
        return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    params = {
        "granularity": granularity,
        "from": dt_to_str(start),
        "to": dt_to_str(end),
        "includeFirst": include_first,
    }

    response = requests.get(
        endpoint,
        params=params,
        headers=headers,
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
