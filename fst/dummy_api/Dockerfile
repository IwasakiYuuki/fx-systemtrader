FROM python

WORKDIR /app
ENV PATH="./env/bin:$PATH"

RUN python -m venv env

COPY . .
RUN pip install --upgrade pip && pip install -e ./
RUN pip install pytest

CMD ["dummy_api"]
