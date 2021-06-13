FROM python

WORKDIR /usr/src/app
ENV PATH="./env/bin:$PATH"

RUN python -m venv env

COPY . .
RUN pip install --upgrade pip && pip install -e ./

CMD ["dummy_api"]
