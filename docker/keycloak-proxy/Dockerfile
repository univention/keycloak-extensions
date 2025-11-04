# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.3-build.20251030@sha256:d8ed2525a5d6bd8294c6705e802c1e1eb49325b4ebbde1750ebb0ce096b12de7

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

COPY . /app
WORKDIR /app

RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
  ca-certificates \
  nodejs \
  npm \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/* \
  && npm install --ignore-scripts \
  && npm cache clean --force

ENV PORT=8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
