# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.6-build.20260911@sha256:15cfacf5a1a5cc09d80b4fd0173408466a4fd6838f74706fd4a5e45bca7bddea

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
