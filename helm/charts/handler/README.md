# handler

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.0](https://img.shields.io/badge/AppVersion-0.1.0-informational?style=flat-square)

A Helm chart for the Keycloak Extensions Handler

**Homepage:** <https://www.univention.de/>

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| appConfig | object | `{"autoExpireRuleInMins":5,"captchaProtectionEnable":"True","deviceProtectionEnable":"True","eventsRetentionPeriod":10,"failedAttemptsForCaptchaTrigger":3,"failedAttemptsForDeviceBlock":5,"failedAttemptsForIpBlock":7,"ipProtectionEnable":"True","logLevel":"DEBUG","mailFrom":"univention@example.org","newDeviceLoginSubject":"New device login","smtpHost":"mail.example.org","smtpPassword":"some_password","smtpPort":"587","smtpUsername":"univention"}` | Application configuration of the Handler |
| appConfig.autoExpireRuleInMins | int | `5` | Minutes to automatically expire actions such as IP and device blocks and reCaptcha prompt |
| appConfig.captchaProtectionEnable | string | `"True"` | Whether to enable reCaptcha prompting protection |
| appConfig.deviceProtectionEnable | string | `"True"` | Whether to enable device blocking |
| appConfig.eventsRetentionPeriod | int | `10` | Minutes to buffer Keycloak events locally, allowing to persist more than the configured in Keycloak |
| appConfig.failedAttemptsForCaptchaTrigger | int | `3` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to enforce reCaptcha prompt |
| appConfig.failedAttemptsForDeviceBlock | int | `5` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger a device block. Should be greater than `FAILED_ATTEMPTS_FOR_CAPTCHA_TRIGGER` if it is enabled |
| appConfig.failedAttemptsForIpBlock | int | `7` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger an IP block. Should be grater than `FAILED_ATTEMPTS_FOR_DEVICE_BLOCK` if it is enabled |
| appConfig.ipProtectionEnable | string | `"True"` | Whether to enable IP blocking |
| appConfig.logLevel | string | `"DEBUG"` | Application LOG level: `DEBUG`, `INFO`, `WARN` or `ERROR` |
| appConfig.mailFrom | string | `"univention@example.org"` | Email to send emails from |
| appConfig.newDeviceLoginSubject | string | `"New device login"` | Subject for email notification to users on New Device Login |
| appConfig.smtpHost | string | `"mail.example.org"` | Email SMTP hostname |
| appConfig.smtpPassword | string | `"some_password"` | Password for SMTP authentication |
| appConfig.smtpPort | string | `"587"` | Email SMTP port |
| appConfig.smtpUsername | string | `"univention"` | Username for SMTP authentication |
| environment | object | `{}` |  |
| fullnameOverride | string | `""` |  |
| global | object | `{"keycloak":{"adminPassword":"univention","adminRealm":null,"adminUsername":"admin","host":"sso.example.com","realm":"ucs"},"postgresql":{"auth":{"database":"bfp","password":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}}` | Global Keycloak Extensions configuration values |
| global.keycloak | object | `{"adminPassword":"univention","adminRealm":null,"adminUsername":"admin","host":"sso.example.com","realm":"ucs"}` | External Keycloak global settings |
| global.keycloak.adminPassword | string | `"univention"` | Admin password for Keycloak admin-cli provided user |
| global.keycloak.adminUsername | string | `"admin"` | Admin user for Keycloak admin-cli |
| global.keycloak.host | string | `"sso.example.com"` | Host where keycloak is accessible (specify port if needed) |
| global.keycloak.realm | string | `"ucs"` | Keycloak realm to listen events on (master allows to listen for all realms) |
| global.postgresql | object | `{"auth":{"database":"bfp","password":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}` | PostgreSQL global settings |
| global.postgresql.auth.database | string | `"bfp"` | Database for the proxy and handler to use |
| global.postgresql.auth.password | string | `"correcthorsebatterystaple"` | Password for the PostgreSQL database |
| global.postgresql.auth.username | string | `"bfp"` | User for the PostgreSQL database |
| global.postgresql.connection.host | string | `"keycloak-extensions-postgresql"` | Hostname or IP address of the server hosting the PostgreSQL database |
| global.postgresql.connection.port | string | `"5432"` | Port number that the PostgreSQL database is exposed on |
| image.imagePullPolicy | string | `"Always"` |  |
| image.registry | string | `"registry.souvap-univention.de"` |  |
| image.repository | string | `"souvap/tooling/images/keycloak-extensions/keycloak-handler"` |  |
| image.tag | string | `"0.1.0"` |  |
| ingress | object | `{"enabled":false}` | Kubernetes ingress |
| ingress.enabled | bool | `false` | Set this to `true` in order to enable the installation on Ingress related objects. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| probes.liveness.enabled | bool | `false` |  |
| probes.readiness.enabled | bool | `false` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | string | `"4"` |  |
| resources.limits.memory | string | `"4Gi"` |  |
| resources.requests.cpu | string | `"250m"` |  |
| resources.requests.memory | string | `"512Mi"` |  |
| securityContext | object | `{}` |  |
| service.enabled | bool | `false` |  |
| tolerations | list | `[]` |  |