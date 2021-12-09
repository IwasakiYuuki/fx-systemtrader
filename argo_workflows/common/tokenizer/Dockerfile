FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir
COPY ./run.sh /workdir

RUN pip install --upgrade pip && pip install \
		janome \
		pandas \
		pyarrow

CMD ["sh", "run.sh"]
