# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

ARG KEYCLOAK_VERSION=26.8.2@sha256:3879c623248408de29a5303178b5816c77e8dfef3890c361f8c0bbeaa979ba3b

FROM maven:3.8.2-openjdk-11 as maven
ARG KEYCLOAK_VERSION
WORKDIR /root/
COPY . .
ENV DEV_KEYCLOAK_VERSION $KEYCLOAK_VERSION
RUN echo "Building for Keycloak $DEV_KEYCLOAK_VERSION"
RUN mvn clean install --file sample-extension

FROM quay.io/keycloak/keycloak:$KEYCLOAK_VERSION
WORKDIR /opt/keycloak/providers
COPY --from=maven /root/sample-extension/target/sample-extension.jar .

WORKDIR /opt/keycloak
COPY ./sample-theme themes/sample

WORKDIR /opt/keycloak
RUN ./bin/kc.sh build
