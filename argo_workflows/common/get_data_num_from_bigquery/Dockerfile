FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir

RUN pip install --upgrade pip && pip install \
		google-cloud-bigquery \
		pandas \
		pyarrow

CMD ["/bin/sh", "-c", "python main.py --project_id=$PROJECT_ID --db_name=$DB_NAME --table_name=$TABLE_NAME --id_field_name=$ID_FIELD_NAME > /tmp/output.txt"]
