FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir

RUN pip install --upgrade pip && \
		pip install \
		google-cloud-storage

ENTRYPOINT ["python"]
CMD ["main.py"]
