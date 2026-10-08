# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025-2026 Univention GmbH

ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base
ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261008@sha256:001595593e7e4d2a2bb29d345c67e91c0800464aa3a2372fa94b40d1ff48d2d5

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
