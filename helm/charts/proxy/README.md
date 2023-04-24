# proxy

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 0.1.0](https://img.shields.io/badge/AppVersion-0.1.0-informational?style=flat-square)

A Helm chart for the Keycloak BFP proxy

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| https://charts.bitnami.com/bitnami | common | ^2.2.2 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| appConfig | object | `{"captchaSiteKey":"some_site_key","logLevel":"debug"}` | Application configuration of the Proxy |
| appConfig.captchaSiteKey | string | `"some_site_key"` | The Google reCaptcha v2 site key generated from [their admin site](https://www.google.com/recaptcha/admin/) |
| appConfig.logLevel | string | `"debug"` | Proxy log level: `debug`, `info`, `warn` or `error` |
| environment | object | `{}` |  |
| fullnameOverride | string | `""` |  |
| global | object | `{"keycloak":{"host":"sso.example.com"},"postgresql":{"auth":{"database":"bfp","password":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}}` | Global Keycloak Extensions configuration values |
| global.keycloak | object | `{"host":"sso.example.com"}` | External Keycloak settings |
| global.keycloak.host | string | `"sso.example.com"` | Host where keycloak is accessible (specify port if needed) |
| global.postgresql | object | `{"auth":{"database":"bfp","password":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}` | PostgreSQL global settings |
| global.postgresql.auth.database | string | `"bfp"` | Database for the proxy and handler to use |
| global.postgresql.auth.password | string | `"correcthorsebatterystaple"` | Password for the PostgreSQL database |
| global.postgresql.auth.username | string | `"bfp"` | User for the PostgreSQL database |
| global.postgresql.connection.host | string | `"keycloak-extensions-postgresql"` | Hostname or IP address of the server hosting the PostgreSQL database |
| global.postgresql.connection.port | string | `"5432"` | Port number that the PostgreSQL database is exposed on |
| image.imagePullPolicy | string | `"Always"` |  |
| image.registry | string | `"registry.souvap-univention.de"` |  |
| image.repository | string | `"souvap/tooling/images/keycloak-extensions/keycloak-proxy"` |  |
| image.tag | string | `"0.1.0"` |  |
| ingress | object | `{"annotations":{},"enabled":true,"ingressClassName":"nginx","paths":[{"path":"/","pathType":"Prefix"}],"tls":{"enabled":true,"secretName":""}}` | Kubernetes ingress |
| ingress.enabled | bool | `true` | Set this to `true` in order to enable the installation on Ingress related objects. |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| probes.liveness.enabled | bool | `false` |  |
| probes.liveness.failureThreshold | int | `3` |  |
| probes.liveness.initialDelaySeconds | int | `120` |  |
| probes.liveness.periodSeconds | int | `30` |  |
| probes.liveness.successThreshold | int | `1` |  |
| probes.liveness.timeoutSeconds | int | `3` |  |
| probes.readiness.enabled | bool | `false` |  |
| probes.readiness.failureThreshold | int | `30` |  |
| probes.readiness.initialDelaySeconds | int | `30` |  |
| probes.readiness.periodSeconds | int | `15` |  |
| probes.readiness.successThreshold | int | `1` |  |
| probes.readiness.timeoutSeconds | int | `3` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | string | `"4"` |  |
| resources.limits.memory | string | `"4Gi"` |  |
| resources.requests.cpu | string | `"250m"` |  |
| resources.requests.memory | string | `"512Mi"` |  |
| securityContext | object | `{}` |  |
| service.enabled | bool | `true` |  |
| service.ports.http.containerPort | int | `8181` |  |
| service.ports.http.port | int | `8181` |  |
| service.ports.http.protocol | string | `"TCP"` |  |
| service.sessionAffinity.enabled | bool | `false` |  |
| service.sessionAffinity.timeoutSeconds | int | `10800` |  |
| service.type | string | `"ClusterIP"` |  |
| tolerations | list | `[]` |  |
