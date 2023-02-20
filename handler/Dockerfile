FROM python:3.8-slim-buster
WORKDIR /usr/app/src
COPY . .
RUN apt update
RUN apt install -y git
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
CMD ["python", "__main__.py"]
