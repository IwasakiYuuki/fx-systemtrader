from google.cloud import storage

bucket_name = "fx-systemtrader-dev-artifacts"
gcs_path = "huga/img.png"
local_path = "/tmp/img.png"

client = storage.Client()
bucket = client.get_bucket(bucket_name)

blob = bucket.blob(gcs_path)
blob.upload_from_filename(local_path)
