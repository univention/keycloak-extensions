# Build custom auth flow
FROM maven:3.8.2-openjdk-11 as maven
WORKDIR /root/
COPY ./reCaptcha-auth-flow ./reCaptcha-auth-flow
RUN mvn clean package --file reCaptcha-auth-flow
RUN mvn install --file reCaptcha-auth-flow

FROM quay.io/keycloak/keycloak:18.0.0
WORKDIR /opt/keycloak/providers
COPY --from=maven /root/reCaptcha-auth-flow/target/reCaptcha-auth-flow.jar .

WORKDIR /opt/keycloak
COPY ./reCaptcha-theme themes/captcha

WORKDIR /opt/keycloak/
RUN ./bin/kc.sh build
