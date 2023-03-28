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

> When accessing via Keycloak API (curl and others), only the IP block will
> ensure Keycloak protection, since device tracking is not available from
> Keycloak API (neither in Keycloak as `device_id` neither with FingerprintJS).

#### Configuration values

- `KEYCLOAK_URL`: The URL to Keycloak, accessible from the proxy container. Example: `http://keycloak:8080`.
- `LOG_LEVEL`: `debug`, `info`, `warn` or `error`.
- `POSTGRES_USER`: This variable stores the username used to authenticate with the PostgreSQL database.
- `POSTGRES_HOST`: This variable stores the hostname or IP address of the server hosting the PostgreSQL database.
- `POSTGRES_DATABASE_NAME`: This variable stores the name of the PostgreSQL database that the application or system will be connecting to.
- `POSTGRES_PASSWORD`: This variable stores the password used to authenticate with the PostgreSQL database.
- `POSTGRES_PORT`: This variable stores the port number that the PostgreSQL database is listening on.
- `CAPTCHA_SITE_KEY`: The Google reCaptcha v2 site key generated from [their admin site](https://www.google.com/recaptcha/admin/).
