FROM python:3.8-slim-buster
WORKDIR /usr/app/src
RUN mkdir -p static/
COPY static/ ./
RUN apt update
RUN apt install -y git curl
RUN curl https://openfpcdn.io/fingerprintjs/v3 > static/fingerprint.js
COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY main.py ./
COPY app.py ./
CMD ["waitress-serve", "--call", "app:create_app"]
