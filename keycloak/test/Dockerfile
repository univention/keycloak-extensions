FROM quay.io/keycloak/keycloak:19.0.2
COPY ./realm-export.json /opt/keycloak/data/import/realm-export.json
WORKDIR /opt/keycloak
USER 1001

RUN bin/kc.sh import --file /opt/keycloak/data/import/realm-export.json --override true