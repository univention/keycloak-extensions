### Handler

This container checks whether some actions need to be taken by the proxy, blocking
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
- `DEVICE_PROTECTION_ENABLE`: Whether to enable device blocking. `True` or `False`.
- `IP_PROTECTION_ENABLE`: Whether to enable IP blocking. `True` or `False`.
- `CAPTCHA_PROTECTION_ENABLE`: Whether to enable reCaptcha prompting protection. `True` or `False`.
- `SMTP_HOST`: Email SMTP hostname. Example: `mail.example.org`.
- `SMTP_PORT`: Email SMTP port. Example: `587`.
- `MAIL_FROM`: Email to send emails from. Example: `univention@example.org`.
- `SMTP_USERNAME`: Username for SMTP authentication. Example: `user`.
- `SMTP_PASSWORD`: Password for SMTP authentication. Example: `somepassword`.
- `NEW_DEVICE_LOGIN_SUBJECT`: Subject for email notification to users on New Device Login. Example: `New device login`.
