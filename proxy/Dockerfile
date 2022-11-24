FROM python:3.8-slim-buster
WORKDIR /usr/app/src
RUN mkdir -p static/
COPY static/fingerprint-3.3.6.js ./static/fingerprint.js
RUN apt update
RUN apt install -y git curl
COPY requirements.txt ./requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
# TODO: cache pip dependencies, for faster image building in CI.
RUN pip3 install -r requirements.txt
COPY main.py ./
COPY app.py ./
CMD ["waitress-serve", "--call", "app:create_app"]
