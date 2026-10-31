# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261029@sha256:ea7a4e49b0e9380901af1a3a6ffb49e50a1f952eb483f3628f75c84a98c09ee6

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
