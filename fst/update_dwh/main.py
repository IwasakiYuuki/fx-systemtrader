import requests
import json
import pandas as pd
from google.cloud import storage, bigquery, bigquery_storage


def update_dwh(request):
    """docstring for update_dwh"""
    bucket_name = "fx-systemtrader-dev-datalake"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    prefix = "rates/USD_JPY/"
    all_blobs = list(storage_client.list_blobs(bucket, prefix=prefix))
    all_blobnames = []
    for blob in all_blobs:
        all_blobnames.append(blob.name)

    bqclient = bigquery.Client()
    query_string = """
    SELECT
        DISTINCT FORMAT_DATE("%Y/%m/%d", time) as time
    FROM
        `fx-systemtrader-dev.fx_features.usd_jpy_s5_candle`
    """
    query_df = (
        bqclient.query(query_string)
        .result()
        .to_dataframe()
    )
    inserted_blobnames = list(
        query_df["time"].map(
            lambda x: prefix + x + ".json"))

    new_blobnames = list(set(all_blobnames) - set(inserted_blobnames))

    table_id = "fx-systemtrader-dev.fx_features.usd_jpy_s5_candle"
    for blobname in new_blobnames:
        blob = bucket.get_blob(blobname)
        if blob:
            byte_data = blob.download_as_bytes()
            dict_data = json.loads(byte_data)
        df = pd.DataFrame(dict_data["candles"])
        df = df.drop("complete", axis=1)
        df["time"] = pd.to_datetime(df["time"])
        df["id"] = df["time"].map(lambda x: int(x.timestamp()))
        if "openMid" in dict_data["candles"][0]:
            df["candleFormat"] = "midpoint"
        else:
            df["candleFormat"] = "bidask"

        load_job = bqclient.load_table_from_dataframe(
            df,
            table_id
        )
        print(load_job.result())

    return
