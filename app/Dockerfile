FROM python:latest

RUN apt-get update && apt-get install -y libhdf5-dev

WORKDIR /code
RUN pip install cmdstanpy==1.2.0
RUN install_cmdstan

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ .

COPY pyproject.toml .
RUN pip install .

COPY .env .

CMD ["main"]
