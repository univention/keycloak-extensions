FROM python:3.8-slim-buster
WORKDIR /usr/app/src
COPY *.py ./
COPY requirements.txt ./
RUN apt-get -qq update && apt-get --assume-yes --no-install-recommends install git && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python3", "./__main__.py"]
