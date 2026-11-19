# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261119@sha256:a9179ffc7390a78d04c46979f2fb555e3ced0cd3ae70c0821b389033e0c6f666

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
