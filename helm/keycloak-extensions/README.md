# keycloak-extensions

![Version: 0.11.0](https://img.shields.io/badge/Version-0.11.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 21.0.1](https://img.shields.io/badge/AppVersion-21.0.1-informational?style=flat-square)

A Helm chart for Kubernetes with its extensions

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| oci://artifacts.software-univention.de/nubus/charts | nubus-common | 0.28.0 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| additionalAnnotations | object | `{}` | Annotations being applied to all resources. |
| additionalLabels | object | `{}` | Additional custom labels being applied to all resources. |
| global | object | `{"imagePullPolicy":null,"imagePullSecrets":[],"imageRegistry":"artifacts.software-univention.de","keycloak":{"realm":""},"nubusDeployment":false,"postgresql":{"connection":{"host":"","port":""}}}` | Global Keycloak Extensions configuration values |
| global.imagePullPolicy | string | `nil` | Define an ImagePullPolicy.  Ref.: https://kubernetes.io/docs/concepts/containers/images/#image-pull-policy  "IfNotPresent" => The image is pulled only if it is not already present locally. "Always" => Every time the kubelet launches a container, the kubelet queries the container image registry to             resolve the name to an image digest. If the kubelet has a container image with that exact digest cached             locally, the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved             digest, and uses that image to launch the container. "Never" => The kubelet does not try fetching the image. If the image is somehow already present locally, the            kubelet attempts to start the container; otherwise, startup fails. |
| global.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| global.imageRegistry | string | `"artifacts.software-univention.de"` | Global image registry |
| global.nubusDeployment | bool | `false` | Indicates wether this chart is part of a Nubus deployment. |
| handler.affinity | object | `{}` |  |
| handler.appConfig | object | `{"autoExpireRuleInMins":1,"captchaProtectionEnable":"False","deviceProtectionEnable":"True","emailNotificationTimezone":"UTC","eventsRetentionPeriod":1,"failedAttemptsForCaptchaTrigger":3,"failedAttemptsForDeviceBlock":5,"failedAttemptsForIpBlock":7,"ipProtectionEnable":"True","logLevel":"INFO","mailFrom":"univention@example.org","newDeviceLoginNotificationEnable":"True","newDeviceLoginSubject":"New device login"}` | Application configuration of the handler |
| handler.appConfig.autoExpireRuleInMins | int | `1` | Minutes to automatically expire actions such as IP and device blocks and reCaptcha prompt |
| handler.appConfig.captchaProtectionEnable | string | `"False"` | Whether to enable reCaptcha prompting protection |
| handler.appConfig.deviceProtectionEnable | string | `"True"` | Whether to enable device blocking |
| handler.appConfig.emailNotificationTimezone | string | `"UTC"` | Timezone for email notifications (see pytz.all_timezones of python library pytz) |
| handler.appConfig.eventsRetentionPeriod | int | `1` | Minutes to buffer Keycloak events locally, allowing to persist more than the configured in Keycloak |
| handler.appConfig.failedAttemptsForCaptchaTrigger | int | `3` | Number of failed login attempts within the minutes of `eventsRetentionPeriod` to enforce reCaptcha prompt |
| handler.appConfig.failedAttemptsForDeviceBlock | int | `5` | Number of failed login attempts within the minutes of `eventsRetentionPeriod` to trigger a device block. Should be greater than `failedAttemptsForCaptchaTrigger` if it is enabled |
| handler.appConfig.failedAttemptsForIpBlock | int | `7` | Number of failed login attempts within the minutes of `eventsRetentionPeriod` to trigger an IP block. Should be greater than `failedAttemptsForDeviceBlock` if it is enabled |
| handler.appConfig.ipProtectionEnable | string | `"True"` | Whether to enable IP blocking |
| handler.appConfig.logLevel | string | `"INFO"` | Application LOG level: `DEBUG`, `INFO`, `WARN` or `ERROR` |
| handler.appConfig.mailFrom | string | `"univention@example.org"` | Email to send emails from |
| handler.appConfig.newDeviceLoginNotificationEnable | string | `"True"` | Whether to enable email notification to users on New Device Login |
| handler.appConfig.newDeviceLoginSubject | string | `"New device login"` | Subject for email notification to users on New Device Login |
| handler.customLivenessProbe | object | `{}` |  |
| handler.customReadinessProbe | object | `{}` |  |
| handler.customStartupProbe | object | `{}` |  |
| handler.enabled | bool | `true` |  |
| handler.environment | object | `{}` |  |
| handler.extraEnvVars | list | `[]` | Array with extra environment variables to add to containers.  extraEnvVars:   - name: FOO     value: "bar" |
| handler.image.pullPolicy | string | `nil` |  |
| handler.image.registry | string | `nil` | Container registry address. |
| handler.image.repository | string | `"nubus-dev/images/keycloak-handler"` |  |
| handler.image.tag | string | `"latest"` |  |
| handler.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| handler.ingress | object | `{"enabled":false}` | Kubernetes ingress |
| handler.ingress.enabled | bool | `false` | Set this to `true` in order to enable the installation on Ingress related objects. |
| handler.lifecycleHooks | object | `{}` |  |
| handler.livenessProbe.command | string | `"exit 0\n"` |  |
| handler.livenessProbe.enabled | bool | `true` |  |
| handler.livenessProbe.failureThreshold | int | `6` |  |
| handler.livenessProbe.initialDelaySeconds | int | `30` |  |
| handler.livenessProbe.periodSeconds | int | `10` |  |
| handler.livenessProbe.successThreshold | int | `1` |  |
| handler.livenessProbe.timeoutSeconds | int | `5` |  |
| handler.nodeSelector | object | `{}` |  |
| handler.podAnnotations | object | `{}` |  |
| handler.podSecurityContext | object | `{}` |  |
| handler.readinessProbe.command | string | `"exit 0\n"` |  |
| handler.readinessProbe.enabled | bool | `true` |  |
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
| handler.securityContext.allowPrivilegeEscalation | bool | `false` |  |
| handler.securityContext.capabilities.drop[0] | string | `"ALL"` |  |
| handler.securityContext.enabled | bool | `true` |  |
| handler.securityContext.privileged | bool | `false` |  |
| handler.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| handler.securityContext.runAsGroup | int | `1000` |  |
| handler.securityContext.runAsNonRoot | bool | `true` |  |
| handler.securityContext.runAsUser | int | `1000` |  |
| handler.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
| handler.service.enabled | bool | `false` |  |
| handler.service.ports | object | `{}` | Additional custom annotations to add to service. |
| handler.serviceAccount | object | `{"annotations":{},"automountServiceAccountToken":false,"create":true,"labels":{},"name":""}` | Additional custom annotations to add to deployments. |
| handler.serviceAccount.labels | object | `{}` | Additional custom labels for the ServiceAccount. |
| handler.startupProbe.command | string | `"exit 0\n"` |  |
| handler.startupProbe.enabled | bool | `true` |  |
| handler.startupProbe.failureThreshold | int | `15` |  |
| handler.startupProbe.initialDelaySeconds | int | `30` |  |
| handler.startupProbe.periodSeconds | int | `10` |  |
| handler.startupProbe.successThreshold | int | `1` |  |
| handler.startupProbe.timeoutSeconds | int | `1` |  |
| handler.terminationGracePeriodSeconds | string | `""` | In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods |
| handler.tolerations | list | `[]` |  |
| imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| keycloak | object | `{"auth":{"existingSecret":{"keyMapping":{"adminPassword":null},"name":""},"masterRealm":"master","password":"","realm":"","username":""},"connection":{"host":""}}` | Keycloak settings. |
| keycloak.auth.existingSecret | object | `{"keyMapping":{"adminPassword":null},"name":""}` | Keycloak password secret reference. |
| keycloak.auth.masterRealm | string | `"master"` | Keycloak master realm. |
| keycloak.auth.password | string | `""` | Keycloak password. |
| keycloak.auth.realm | string | `""` | Keycloak realm. |
| keycloak.auth.username | string | `""` | Keycloak user. |
| keycloak.connection | object | `{"host":""}` | Connection parameters. |
| keycloak.connection.host | string | `""` | Keycloak host. |
| postgresql | object | `{"auth":{"database":"","existingSecret":{"keyMapping":{"password":null},"name":""},"password":"","username":""},"connection":{"customca":"","host":"","pathCA":"/etc/ssl/certs/rootca.pem","port":"","ssl":"false"}}` | PostgreSQL settings. |
| postgresql.auth.database | string | `""` | PostgreSQL database. |
| postgresql.auth.existingSecret | object | `{"keyMapping":{"password":null},"name":""}` | PostgreSQL password secret reference. |
| postgresql.auth.password | string | `""` | PostgreSQL user password. |
| postgresql.auth.username | string | `""` | PostgreSQL user. |
| postgresql.connection | object | `{"customca":"","host":"","pathCA":"/etc/ssl/certs/rootca.pem","port":"","ssl":"false"}` | Connection parameters. |
| postgresql.connection.customca | string | `""` | CustomCA certificate |
| postgresql.connection.host | string | `""` | PostgreSQL host. |
| postgresql.connection.pathCA | string | `"/etc/ssl/certs/rootca.pem"` | Path to CA |
| postgresql.connection.port | string | `""` | PostgreSQL port. |
| postgresql.connection.ssl | string | `"false"` | PostgreSQL SSL flag |
| proxy.affinity | object | `{}` |  |
| proxy.appConfig | object | `{"captcha":{"captchaSecretKey":"some_secret_key","captchaSiteKey":"some_site_key","existingSecret":{"keyMapping":{"secret_key":null,"site_key":null},"name":""}},"logLevel":"info"}` | Application configuration of the proxy |
| proxy.appConfig.captcha | object | `{"captchaSecretKey":"some_secret_key","captchaSiteKey":"some_site_key","existingSecret":{"keyMapping":{"secret_key":null,"site_key":null},"name":""}}` | The Google reCaptcha v2 site key generated from [their admin site](https://www.google.com/recaptcha/admin/) |
| proxy.appConfig.logLevel | string | `"info"` | Proxy log level: `debug`, `info`, `warn` or `error` |
| proxy.customLivenessProbe | object | `{}` |  |
| proxy.customReadinessProbe | object | `{}` |  |
| proxy.customStartupProbe | object | `{}` |  |
| proxy.enabled | bool | `true` |  |
| proxy.environment | object | `{}` |  |
| proxy.extraEnvVars | list | `[]` | Array with extra environment variables to add to containers.  extraEnvVars:   - name: FOO     value: "bar" |
| proxy.image.pullPolicy | string | `nil` |  |
| proxy.image.registry | string | `nil` | Container registry address. |
| proxy.image.repository | string | `"nubus-dev/images/keycloak-proxy"` |  |
| proxy.image.tag | string | `"latest"` |  |
| proxy.imagePullSecrets | list | `[]` | Credentials to fetch images from private registry. Ref: https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/  imagePullSecrets:   - "docker-registry" |
| proxy.ingress | object | `{"annotations":{"nginx.ingress.kubernetes.io/proxy-buffer-size":"8k","nginx.org/proxy-buffer-size":"8k"},"certManager":{"enabled":true,"issuerRef":{"kind":"ClusterIssuer","name":""}},"enabled":true,"ingressClassName":"","paths":[{"path":"/admin","pathType":"Prefix"},{"path":"/realms","pathType":"Prefix"},{"path":"/resources","pathType":"Prefix"},{"path":"/fingerprintjs","pathType":"Prefix"}],"tls":{"enabled":true,"secretName":""}}` | Kubernetes ingress |
| proxy.ingress.certManager.enabled | bool | `true` | Enable cert-manager.io annotaion. |
| proxy.ingress.certManager.issuerRef.kind | string | `"ClusterIssuer"` | Type of Issuer, f.e. "Issuer" or "ClusterIssuer". |
| proxy.ingress.certManager.issuerRef.name | string | `""` | Name of cert-manager.io Issuer resource. |
| proxy.ingress.enabled | bool | `true` | Set this to `true` in order to enable the installation on Ingress related objects. |
| proxy.lifecycleHooks | object | `{}` |  |
| proxy.livenessProbe.enabled | bool | `true` |  |
| proxy.livenessProbe.failureThreshold | int | `6` |  |
| proxy.livenessProbe.initialDelaySeconds | int | `30` |  |
| proxy.livenessProbe.periodSeconds | int | `10` |  |
| proxy.livenessProbe.successThreshold | int | `1` |  |
| proxy.livenessProbe.timeoutSeconds | int | `5` |  |
| proxy.logVolume.sizeLimit | string | `"1Gi"` | Size limit of the emptyDir volume holding the log file. |
| proxy.nodeSelector | object | `{}` |  |
| proxy.podAnnotations | object | `{}` |  |
| proxy.podSecurityContext | object | `{}` |  |
| proxy.readinessProbe.enabled | bool | `true` |  |
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
| proxy.securityContext.enabled | bool | `true` |  |
| proxy.securityContext.privileged | bool | `false` |  |
| proxy.securityContext.readOnlyRootFilesystem | bool | `true` |  |
| proxy.securityContext.runAsGroup | int | `1000` |  |
| proxy.securityContext.runAsNonRoot | bool | `true` |  |
| proxy.securityContext.runAsUser | int | `1000` |  |
| proxy.securityContext.seccompProfile.type | string | `"RuntimeDefault"` |  |
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
| proxy.startupProbe.enabled | bool | `true` |  |
| proxy.startupProbe.failureThreshold | int | `15` |  |
| proxy.startupProbe.initialDelaySeconds | int | `30` |  |
| proxy.startupProbe.periodSeconds | int | `10` |  |
| proxy.startupProbe.successThreshold | int | `1` |  |
| proxy.startupProbe.timeoutSeconds | int | `1` |  |
| proxy.terminationGracePeriodSeconds | string | `""` | In seconds, time the given to the pod needs to terminate gracefully. Ref: https://kubernetes.io/docs/concepts/workloads/pods/pod/#termination-of-pods |
| proxy.tolerations | list | `[]` |  |
| smtp | object | `{"auth":{"enabled":true,"existingSecret":{"keyMapping":{"password":null},"name":""},"password":"","username":"keycloak-extensions"},"connection":{"host":"","port":"587","ssl":false,"starttls":true}}` | SMTP settings. |
| smtp.auth.enabled | bool | `true` | Enable SMTP authentication |
| smtp.auth.existingSecret | object | `{"keyMapping":{"password":null},"name":""}` | SMTP password secret reference. |
| smtp.auth.password | string | `""` | Password for SMTP authentication |
| smtp.auth.username | string | `"keycloak-extensions"` | Username for SMTP authentication |
| smtp.connection | object | `{"host":"","port":"587","ssl":false,"starttls":true}` | Connection parameters. |
| smtp.connection.host | string | `""` | Email SMTP hostname |
| smtp.connection.port | string | `"587"` | Email SMTP port |
| smtp.connection.ssl | bool | `false` | Require SSL/TLS encryption for connection. |
| smtp.connection.starttls | bool | `true` | Use StartTLS for traffic encryption: |
