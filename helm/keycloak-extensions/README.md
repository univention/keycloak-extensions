# keycloak-extensions

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 21.0.1](https://img.shields.io/badge/AppVersion-21.0.1-informational?style=flat-square)

A Helm chart for Kubernetes with its extensions

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | common | ^2.x.x |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global | object | `{"imageRegistry":"gitregistry.knut.univention.de","keycloak":{"adminPassword":"","adminRealm":null,"adminUsername":"","host":"","realm":""},"postgresql":{"auth":{"database":"","password":"","postgresPassword":"","username":""},"connection":{"host":"","port":""}}}` | Global Keycloak Extensions configuration values |
| global.imageRegistry | string | `"gitregistry.knut.univention.de"` | Container registry address. |
| global.keycloak | object | `{"adminPassword":"","adminRealm":null,"adminUsername":"","host":"","realm":""}` | External Keycloak settings |
| global.keycloak.adminPassword | string | `""` | Admin password for Keycloak admin-cli provided user |
| global.keycloak.adminUsername | string | `""` | Admin user for Keycloak admin-cli |
| global.keycloak.host | string | `""` | Host where keycloak is accessible (specify port if needed) |
| global.keycloak.realm | string | `""` | Keycloak realm to listen events on (master allows to listen for all realms) |
| global.postgresql | object | `{"auth":{"database":"","password":"","postgresPassword":"","username":""},"connection":{"host":"","port":""}}` | PostgreSQL settings |
| global.postgresql.auth | object | `{"database":"","password":"","postgresPassword":"","username":""}` | Authentication details |
| global.postgresql.auth.database | string | `""` | Database for the proxy and handler to use |
| global.postgresql.auth.password | string | `""` | Password for the PostgreSQL database |
| global.postgresql.auth.postgresPassword | string | `""` | Currently unused |
| global.postgresql.auth.username | string | `""` | User for the PostgreSQL database |
| global.postgresql.connection | object | `{"host":"","port":""}` | Connextion details |
| global.postgresql.connection.host | string | `""` | Hostname or IP address of the server hosting the PostgreSQL database |
| global.postgresql.connection.port | string | `""` | Port number that the PostgreSQL database is exposed on |
| handler.additionalAnnotations | object | `{}` | Additional custom annotations to add to deployments. |
| handler.affinity | object | `{}` |  |
| handler.appConfig | object | `{"autoExpireRuleInMins":5,"captchaProtectionEnable":"True","deviceProtectionEnable":"True","eventsRetentionPeriod":10,"failedAttemptsForCaptchaTrigger":3,"failedAttemptsForDeviceBlock":5,"failedAttemptsForIpBlock":7,"ipProtectionEnable":"True","logLevel":"DEBUG","mailFrom":"univention@example.org","newDeviceLoginSubject":"New device login","smtpHost":"mail.example.org","smtpPassword":"some_password","smtpPort":"587","smtpUsername":"univention"}` | Application configuration of the handler |
| handler.appConfig.autoExpireRuleInMins | int | `5` | Minutes to automatically expire actions such as IP and device blocks and reCaptcha prompt |
| handler.appConfig.captchaProtectionEnable | string | `"True"` | Whether to enable reCaptcha prompting protection |
| handler.appConfig.deviceProtectionEnable | string | `"True"` | Whether to enable device blocking |
| handler.appConfig.eventsRetentionPeriod | int | `10` | Minutes to buffer Keycloak events locally, allowing to persist more than the configured in Keycloak |
| handler.appConfig.failedAttemptsForCaptchaTrigger | int | `3` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to enforce reCaptcha prompt |
| handler.appConfig.failedAttemptsForDeviceBlock | int | `5` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger a device block. Should be greater than `FAILED_ATTEMPTS_FOR_CAPTCHA_TRIGGER` if it is enabled |
| handler.appConfig.failedAttemptsForIpBlock | int | `7` | Number of failed login attempts within the minutes of `EVENTS_RETENTION_MINUTES` to trigger an IP block. Should be grater than `FAILED_ATTEMPTS_FOR_DEVICE_BLOCK` if it is enabled |
| handler.appConfig.ipProtectionEnable | string | `"True"` | Whether to enable IP blocking |
| handler.appConfig.logLevel | string | `"DEBUG"` | Application LOG level: `DEBUG`, `INFO`, `WARN` or `ERROR` |
| handler.appConfig.mailFrom | string | `"univention@example.org"` | Email to send emails from |
| handler.appConfig.newDeviceLoginSubject | string | `"New device login"` | Subject for email notification to users on New Device Login |
| handler.appConfig.smtpHost | string | `"mail.example.org"` | Email SMTP hostname |
| handler.appConfig.smtpPassword | string | `"some_password"` | Password for SMTP authentication |
| handler.appConfig.smtpPort | string | `"587"` | Email SMTP port |
| handler.appConfig.smtpUsername | string | `"univention"` | Username for SMTP authentication |
| handler.customLivenessProbe | object | `{}` |  |
| handler.customReadinessProbe | object | `{}` |  |
| handler.customStartupProbe | object | `{}` |  |
| handler.environment | object | `{}` |  |
| handler.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| handler.image.registry | string | `"gitregistry.knut.univention.de"` |  |
| handler.image.repository | string | `"univention/components/keycloak-extensions/keycloak-handler"` |  |
| handler.image.tag | string | `"latest"` |  |
| handler.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| handler.ingress | object | `{"enabled":false}` | Kubernetes ingress |
| handler.ingress.enabled | bool | `false` | Set this to `true` in order to enable the installation on Ingress related objects. |
| handler.lifecycleHooks | object | `{}` |  |
| handler.livenessProbe.command | string | `"exit 0\n"` |  |
| handler.livenessProbe.enabled | bool | `false` |  |
| handler.livenessProbe.failureThreshold | int | `6` |  |
| handler.livenessProbe.initialDelaySeconds | int | `30` |  |
| handler.livenessProbe.periodSeconds | int | `10` |  |
| handler.livenessProbe.successThreshold | int | `1` |  |
| handler.livenessProbe.timeoutSeconds | int | `5` |  |
| handler.nodeSelector | object | `{}` |  |
| handler.podAnnotations | object | `{}` |  |
| handler.podSecurityContext | object | `{}` |  |
| handler.readinessProbe.command | string | `"exit 0\n"` |  |
| handler.readinessProbe.enabled | bool | `false` |  |
| handler.readinessProbe.failureThreshold | int | `6` |  |
| handler.readinessProbe.initialDelaySeconds | int | `5` |  |
| handler.readinessProbe.periodSeconds | int | `10` |  |
| handler.readinessProbe.successThreshold | int | `1` |  |
| handler.readinessProbe.timeoutSeconds | int | `5` |  |
| handler.replicaCount | int | `1` |  |
| handler.resources.limits.cpu | string | `"4"` |  |
| handler.resources.limits.memory | string | `"4Gi"` |  |
| handler.resources.requests.cpu | string | `"250m"` |  |
| handler.resources.requests.memory | string | `"512Mi"` |  |
| handler.securityContext | object | `{}` |  |
| handler.service.additionalAnnotations | object | `{}` | Additional custom annotations to add to service. |
| handler.service.enabled | bool | `false` |  |
| handler.serviceAccount.annotations | object | `{}` |  |
| handler.serviceAccount.automountServiceAccountToken | bool | `false` |  |
| handler.serviceAccount.create | bool | `true` |  |
| handler.serviceAccount.labels | object | `{}` | Additional custom labels for the ServiceAccount. |
| handler.serviceAccount.name | string | `""` |  |
| handler.startupProbe.command | string | `"exit 0\n"` |  |
| handler.startupProbe.enabled | bool | `false` |  |
| handler.startupProbe.failureThreshold | int | `15` |  |
| handler.startupProbe.initialDelaySeconds | int | `30` |  |
| handler.startupProbe.periodSeconds | int | `10` |  |
| handler.startupProbe.successThreshold | int | `1` |  |
| handler.startupProbe.timeoutSeconds | int | `1` |  |
| handler.terminationGracePeriodSeconds | string | `""` | In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods |
| handler.tolerations | list | `[]` |  |
| keycloak.adminPassword | string | `""` |  |
| keycloak.adminRealm | string | `""` |  |
| keycloak.adminUsername | string | `""` |  |
| keycloak.host | string | `""` |  |
| keycloak.realm | string | `""` |  |
| postgresql | object | `{"auth":{"database":"","password":"","username":""},"connection":{"host":"","port":""}}` | PostgreSQL settings.  The bitnami helm chart does contain all details of what can be configured: https://github.com/bitnami/charts/tree/main/bitnami/postgresql |
| proxy.additionalAnnotations | object | `{}` | Additional custom annotations to add to deployments. |
| proxy.affinity | object | `{}` |  |
| proxy.appConfig | object | `{"captchaSecretKey":"some_secret_key","captchaSiteKey":"some_site_key","logLevel":"debug"}` | Application configuration of the proxy |
| proxy.appConfig.captchaSiteKey | string | `"some_site_key"` | The Google reCaptcha v2 site key generated from [their admin site](https://www.google.com/recaptcha/admin/) |
| proxy.appConfig.logLevel | string | `"debug"` | Proxy log level: `debug`, `info`, `warn` or `error` |
| proxy.customLivenessProbe | object | `{}` |  |
| proxy.customReadinessProbe | object | `{}` |  |
| proxy.customStartupProbe | object | `{}` |  |
| proxy.environment | object | `{}` |  |
| proxy.image.imagePullPolicy | string | `"IfNotPresent"` |  |
| proxy.image.registry | string | `"gitregistry.knut.univention.de"` |  |
| proxy.image.repository | string | `"univention/components/keycloak-extensions/keycloak-proxy"` |  |
| proxy.image.tag | string | `"latest"` |  |
| proxy.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| proxy.ingress | object | `{"annotations":{},"enabled":true,"ingressClassName":"nginx","paths":[{"path":"/","pathType":"Prefix"}],"tls":{"enabled":true,"secretName":""}}` | Kubernetes ingress |
| proxy.ingress.enabled | bool | `true` | Set this to `true` in order to enable the installation on Ingress related objects. |
| proxy.lifecycleHooks | object | `{}` |  |
| proxy.livenessProbe.enabled | bool | `false` |  |
| proxy.livenessProbe.failureThreshold | int | `6` |  |
| proxy.livenessProbe.initialDelaySeconds | int | `30` |  |
| proxy.livenessProbe.periodSeconds | int | `10` |  |
| proxy.livenessProbe.successThreshold | int | `1` |  |
| proxy.livenessProbe.timeoutSeconds | int | `5` |  |
| proxy.nodeSelector | object | `{}` |  |
| proxy.podAnnotations | object | `{}` |  |
| proxy.podSecurityContext | object | `{}` |  |
| proxy.readinessProbe.enabled | bool | `false` |  |
| proxy.readinessProbe.failureThreshold | int | `6` |  |
| proxy.readinessProbe.initialDelaySeconds | int | `5` |  |
| proxy.readinessProbe.periodSeconds | int | `10` |  |
| proxy.readinessProbe.successThreshold | int | `1` |  |
| proxy.readinessProbe.timeoutSeconds | int | `5` |  |
| proxy.replicaCount | int | `1` |  |
| proxy.resources.limits.cpu | string | `"4"` |  |
| proxy.resources.limits.memory | string | `"4Gi"` |  |
| proxy.resources.requests.cpu | string | `"250m"` |  |
| proxy.resources.requests.memory | string | `"512Mi"` |  |
| proxy.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| proxy.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| proxy.securityContext.privileged | bool | `false` |  |
| proxy.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| proxy.securityContext.runAsGroup | int | `1000` |  |
| proxy.securityContext.runAsNonRoot | bool | `true` |  |
| proxy.securityContext.runAsUser | int | `1000` |  |
| proxy.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| proxy.service.additionalAnnotations | object | `{}` | Additional custom annotations to add to service. |
| proxy.service.enabled | bool | `true` |  |
| proxy.service.ports.http.containerPort | int | `8181` |  |
| proxy.service.ports.http.port | int | `8181` |  |
| proxy.service.ports.http.protocol | string | `"TCP"` |  |
| proxy.service.sessionAffinity.enabled | bool | `false` |  |
| proxy.service.sessionAffinity.timeoutSeconds | int | `10800` |  |
| proxy.service.type | string | `"ClusterIP"` |  |
| proxy.serviceAccount.annotations | object | `{}` |  |
| proxy.serviceAccount.automountServiceAccountToken | bool | `false` |  |
| proxy.serviceAccount.create | bool | `true` |  |
| proxy.serviceAccount.labels | object | `{}` | Additional custom labels for the ServiceAccount. |
| proxy.serviceAccount.name | string | `""` |  |
| proxy.startupProbe.enabled | bool | `false` |  |
| proxy.startupProbe.failureThreshold | int | `15` |  |
| proxy.startupProbe.initialDelaySeconds | int | `30` |  |
| proxy.startupProbe.periodSeconds | int | `10` |  |
| proxy.startupProbe.successThreshold | int | `1` |  |
| proxy.startupProbe.timeoutSeconds | int | `1` |  |
| proxy.terminationGracePeriodSeconds | string | `""` | In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods |
| proxy.tolerations | list | `[]` |  |
