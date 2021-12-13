FROM python:3.9.7

WORKDIR /workdir

RUN apt-get update -y && apt-get install -y \
		build-essential

RUN pip install --upgrade pip && pip install \
		numpy \
		pandas

COPY main.py /workdir/
