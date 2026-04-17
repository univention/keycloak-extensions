# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.5-build.20260417@sha256:01d93ca22e4312a1d3d47322bc93448e5cf0b55206ec5b3e019493f632debe36

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
