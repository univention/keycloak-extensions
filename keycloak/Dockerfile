# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

ARG KEYCLOAK_VERSION=19.0.3@sha256:979743420b63a7c45fcd2cbaf0a0c528473fd28d6f4cd627969e1b4c39f6fcc0

FROM maven:3.8.2-openjdk-11@sha256:9d2f1b652dd5e427fc2686e11bd832d4d8f7c412632ff5631d48d58ed34d14db as maven
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
