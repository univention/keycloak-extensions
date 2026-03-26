# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.5-build.20260326@sha256:8381ca70cdad990e82dd44a9cb58a04be22cef60ef50a025a42a7620dcb09a9e

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

COPY . /app
WORKDIR /app

RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
  ca-certificates \
  nodejs \
  npm \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/* \
  && npm install --ignore-scripts --omit=dev \
  && npm cache clean --force

ENV PORT=8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
