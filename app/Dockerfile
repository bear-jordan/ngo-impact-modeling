FROM python:latest

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

COPY pyproject.toml .
RUN pip install .

CMD ["gen_data"]
