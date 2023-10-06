FROM gitregistry.knut.univention.de/univention/customers/dataport/upx/container-ucs-base/ucs-base-test-520-dev:v0.6.0
WORKDIR /usr/app/src
COPY . .
RUN apt update \
    && apt install -y git \
    && apt install -y python3 \
    && apt install -y python3-pip \
    && pip3 install --break-system-packages -r requirements.txt \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*
CMD ["python3", "__main__.py"]
