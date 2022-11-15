FROM python:3.8-slim-buster
WORKDIR /usr/app/src
COPY main.py ./
COPY app.py ./
COPY requirements.txt ./
RUN mkdir -p static/
COPY static/ ./
RUN apt update
RUN apt install -y git curl
RUN curl https://openfpcdn.io/fingerprintjs/v3 > static/fingerprint.js
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["waitress-serve", "--call", "CoreApi:create_app"]
