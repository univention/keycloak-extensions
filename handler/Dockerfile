FROM python:3.8-slim-buster
WORKDIR /usr/app/src
COPY . ./
RUN apt-get -qq update && apt-get --assume-yes --no-install-recommends install git && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
ENV LOG_LEVEL INFO
CMD [ "python", "__main__.py"]
