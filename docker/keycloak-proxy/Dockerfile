# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-520
ARG UCS_BASE_IMAGE_TAG=0.11.3

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG}

COPY . /app
WORKDIR /app

RUN apt-get -qq update \
  && apt-get --assume-yes --verbose-versions --no-install-recommends install \
    nodejs \
    npm \
  && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN npm install \
  && npm cache clean --force

ENV PORT 8181
EXPOSE 8181

CMD ["nodejs", "app.js"]
