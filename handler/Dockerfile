ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-520
ARG UCS_BASE_IMAGE_TAG=v0.7.2

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

WORKDIR /usr/app/src
COPY . .
RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    git \
    python3-minimal \
    python3-pip \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV PIP_BREAK_SYSTEM_PACKAGES=1
RUN pip3 install -r requirements.txt
CMD ["python3", "__main__.py"]
