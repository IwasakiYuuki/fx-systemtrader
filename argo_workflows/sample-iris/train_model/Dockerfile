FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir

RUN pip install --upgrade pip && \
		pip install \
		numpy \
		scikit-learn \
		pandas \
		matplotlib

ENTRYPOINT ["python"]
CMD ["main.py"]
