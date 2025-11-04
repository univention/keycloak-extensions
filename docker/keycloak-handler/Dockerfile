# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.3-build.20251030@sha256:d8ed2525a5d6bd8294c6705e802c1e1eb49325b4ebbde1750ebb0ce096b12de7

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
