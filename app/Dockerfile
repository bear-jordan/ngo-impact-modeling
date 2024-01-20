FROM python:latest

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN install_cmdstan

COPY src/ .

COPY pyproject.toml .
RUN pip install .

CMD ["main"]
