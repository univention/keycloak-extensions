# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

ARG KEYCLOAK_VERSION=26.7.3@sha256:ff4257d0d64efbe99ed1ddfaf07765cc3c36dc7518bf8324d41961327f441c54

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
