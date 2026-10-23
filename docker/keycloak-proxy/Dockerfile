# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261022@sha256:6b488e8625d0fc0a45f0945703c5cbbb1753ac904dfde1c3a668ad472d5dc7f8

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
