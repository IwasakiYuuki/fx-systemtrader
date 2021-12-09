FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir
COPY ./run.sh /workdir

RUN pip install --upgrade pip && pip install \
		google-cloud-bigquery \
		pandas \
		pyarrow

CMD ["python", "main.py"]
