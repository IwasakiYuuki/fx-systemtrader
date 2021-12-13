FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-runtime

WORKDIR /workdir

RUN apt-get update -y && apt-get install -y \
		wget \
		build-essential \
		mecab \
		libmecab-dev \
		mecab-ipadic \
		mecab-ipadic-utf8

RUN pip install --upgrade pip && pip install \
		numpy \
		pandas \
		mlflow \
		transformers \
		mecab-python3 \
		fugashi \
		ipadic \
		google-cloud-storage
RUN pip install --ignore-installed kubernetes

COPY main.py /workdir/
