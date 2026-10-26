# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2023 Univention GmbH

FROM quay.io/keycloak/keycloak:19.0.2
COPY ./realm-export.json /opt/keycloak/data/import/realm-export.json
WORKDIR /opt/keycloak
USER 1001
# The JDK 17 in Keycloak 19 throws a NullPointerException reading cgroup v2 limits on current CI nodes
ENV JAVA_OPTS_APPEND=-XX:-UseContainerSupport
RUN bin/kc.sh import --file /opt/keycloak/data/import/realm-export.json --override true
