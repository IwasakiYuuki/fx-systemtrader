FROM python:3.9.7

WORKDIR /workdir
COPY ./main.py /workdir

RUN pip install --upgrade pip && pip install \
		numpy \
		gensim==3.7.0 \
		scikit-learn \
		pandas \
		pyarrow

CMD ["python", "main.py"]
