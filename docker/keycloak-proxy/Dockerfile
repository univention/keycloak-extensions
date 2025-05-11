# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base-521
ARG UCS_BASE_IMAGE_TAG=0.17.3-build-2025-05-11

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

COPY . /app
WORKDIR /app

RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    nodejs \
    npm \
    ca-certificates \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN npm install \
  && npm cache clean --force

ENV PORT 8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
