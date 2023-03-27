# KeyCloak Extensions

## Introduction

This is the repository for Keycloak Extensions, currently being:

1. Brute-Force Protection
2. New Device Login

### Brute-Force Protection (BFP)

This extension aims to protect Keycloak from brute-force attacks.

> In cryptography, a brute-force attack consists of an attacker submitting many passwords or passphrases with the hope of eventually guessing correctly.

### New Device Login (NDL)

This extension aims to notify users by email when they login from a new device.

# Setup

## Configure Keycloak

### Events

We need user events to be enabled. In order to do so:

#### Keycloak > 18

1. Access `http://localhost:5050/admin`.
2. Click `Administration Console`.
3. Access with user `admin` and password `univention`.
4. Click `Realm settings` on the left menu.
5. Go to `Events` tab.
6. Under `User events settings` set `Save events` to `ON`.
7. You can set an expiration time for events, but it is not needed for local testing.
8. For now we only need `LOGIN_ERROR` and `LOGIN`, but no need to disable the other 111 event types.

#### Keycloak <= 18

1. Access `http://localhost:5050/admin`.
2. Click `Administration Console`.
3. Access with user `admin` and password `univention`.
4. Click `Events` on the left menu, towards the bottom.
5. Go into `Config` tab.
6. Under `Login Events Settings`, set `Save Events` to `ON`.
7. Save.
8. (Not needed) You can set an expiration time for events, but it is not needed for local testing.
9. (Not needed) For now we only need `LOGIN_ERROR` and `LOGIN`, but no need to disable the other 111 event types.

> Any changes to `docker-compose.yaml` will affect this steps.

### Configure reCaptcha

In order for reCaptcha to work, we need to tweak two things on Keycloak:

1. Go to `Realm settings > Security Defenses` and set:
2. `X-Frame-Options` to `ALLOW-FROM https://www.google.com`
3. `Content-Security-Policy` to `frame-src 'self' https://www.google.com; frame-ancestors 'self'; object-src 'none';`
4. Save.

Now you need to check that your proxy gets the environment variable `CAPTCHA_SITE_KEY`.
For localhost, I lend you this one: `6LcUyZkiAAAAAHo98CowhZFoc-E-3yeo38Hs1HSB`, but you
may want to grab one from [here](https://www.google.com/recaptcha/admin/).

Currently only Google reCaptcha is supported, but Cloudflare and others are easy to integrate.

## Local setup

`docker compose up -d keycloak database`  
`docker compose up -d proxy handler`

You can access:

- Keycloak at `http://localhost:5050` (only for configuration).
- Proxied Keycloak at `http://localhost:8181` (protected by proxy).
- Handler will be polling Keycloak directly (without the proxy).

# Components

## Architecture

![Architecture](images/architecture.png)

## Proxy

The proxy container is the only one exposed, acting as an entrypoint to Keycloak.
It acts as a proxy to Keycloak, which is not directly exposed. Usually it just
proxies all the requests, but it sometimes it does some magic:

1. **Fingerprint requests to track devices**: by injecting
   [FingerprintJS](https://github.com/fingerprintjs/fingerprintjs) into the login
   page, it sets a cookie. It tracks the device even when the cookie is cleared.
2. **Block requests based on IP**: when such action is read on the database,
   the proxy will block the login requests. This action expires automatically
   after the default configured time.
3. **Block requests based on device**: when such action is read on the database,
   the proxy will block the login requests. This action expires automatically
   after the default configured time.
4. **Injects the reCaptcha into the login form**: when such action is read on
   the database, the proxy will block the login requests. This action expires
   automatically after the default configured time.
5. **Saves relation between a device and the new logged-in user**: so that the
   handler service can notify the user by email about the login.

#### Configuration values

- `KEYCLOAK_URL`: The URL to Keycloak, accessible from the proxy container. Example: `https://keycloak:8080`.
- `LOG_LEVEL`: `debug`, `info`, `warn` or `error`.
- `POSTGRES_USER`: This variable stores the username used to authenticate with the PostgreSQL database.
- `POSTGRES_HOST`: This variable stores the hostname or IP address of the server hosting the PostgreSQL database.
- `POSTGRES_DATABASE_NAME`: This variable stores the name of the PostgreSQL database that the application or system will be connecting to.
- `POSTGRES_PASSWORD`: This variable stores the password used to authenticate with the PostgreSQL database.
- `POSTGRES_PORT`: This variable stores the port number that the PostgreSQL database is listening on.
- `CAPTCHA_SITE_KEY`: The Google reCaptcha v2 site key generated from [their admin site](https://www.google.com/recaptcha/admin/).

### Handler

This container checks wether some actions need to be taken by the proxy, blocking
an IP, a device or enforcing reCaptcha. The handler does the following:

1. Polls events from Keycloak every second.
2. Check Keycloak events against rules.
3. Saves the decided actions on the database, which the proxy will use.
4. Sets expiration time of actions to 5 minutes (configurable) automatically.
5. Deletes expired actions from the database.
6. TODO: Notifies the administrator if failed login attempts rate is exceeded.
7. Sends an email to the user when there is a New Device Login.

#### Configuration values

- `KC_AUTH_URL`: URL for Keycloak admin authentication, usually `http://keycloak:8080/admin`.
- `KC_USER`: user for the realm.
- `KC_PASS`: password for the provided user.
- `KC_REALM`: realm to listen events on (master allows to listen for all realms).
- `POSTGRES_USER`: This variable stores the username used to authenticate with the PostgreSQL database.
- `POSTGRES_HOST`: This variable stores the hostname or IP address of the server hosting the PostgreSQL database.
- `POSTGRES_DATABASE_NAME`: This variable stores the name of the PostgreSQL database that the application or system will be connecting to.
- `POSTGRES_PASSWORD`: This variable stores the password used to authenticate with the PostgreSQL database.
- `POSTGRES_PORT`: This variable stores the port number that the PostgreSQL database is listening on.
- `LOG_LEVEL`: `DEBUG`, `INFO`, `WARN` or `ERROR`.
- `FAILED_ATTEMPTS_FOR_IP_BLOCK`: Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger an IP block. Should be grater than `FAILED_ATTEMPTS_FOR_DEVICE_BLOCK` if it is enabled. Example: `7`.
- `FAILED_ATTEMPTS_FOR_DEVICE_BLOCK`: Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger a device block. Should be greater than `FAILED_ATTEMPTS_FOR_CAPTCHA_TRIGGER` if it is enabled. Example: `5`.
- `FAILED_ATTEMPTS_FOR_CAPTCHA_TRIGGER`: Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to enforce reCaptcha prompt. Example: `3`.
- `EVENTS_RETENTION_MINUTES`: Minutes to buffer Keycloak events locally, allowing to persist more than the configured in Keycloak. Example: `1`.
- `AUTO_EXPIRE_RULE_IN_MINS`: Minutes to automatically expire actions such as IP and device blocks and reCaptcha prompt. Example: `1`.
- `DEVICE_PROTECTION_ENABLE`: Wether to enable device blocking. `True` or `False`.
- `IP_PROTECTION_ENABLE`: Wether to enable IP blocking. `True` or `False`.
- `CAPTCHA_PROTECTION_ENABLE`: Wether to enable reCaptcha prompting protection. `True` or `False`.
- `SMTP_HOST`: Email SMTP hostname. Example: `mail.example.org`.
- `SMTP_PORT`: Email SMTP port. Example: `587`.
- `MAIL_FROM`: Email to send emails from. Example: `univention@example.org`.
- `SMTP_USERNAME`: Username for SMTP authentication. Example: `user`.
- `SMTP_PASSWORD`: Password for SMTP authentication. Example: `somepassword`.
- `NEW_DEVICE_LOGIN_SUBJECT`: Subject for email notification to users on New Device Login. Example: `New device login`.

## Future lines of work

1. Keycloak event monitoring on Grafana (sucessful logins, failed login attempts...)
2. UDM integration
3. Whitelists
4. Blacklists
