# Helm Chart for Keycloak Extensions

Allows to install Keycloak with brute force protection into a kubernetes cluster.

## Prerequisites

- The images are available at the SouvAP container registry with the same name:

  https://gitlab.souvap-univention.de/souvap/tooling/images/keycloak-extensions/container_registry

## Run

Copy the `values.yaml` file and adjust for your needs.

- Note the version/tag which you want to run and adjust them in `values.yaml` accordingly.

- Decide whether to use the PostgreSQL from the sub-chart, or provide your own.

  - In case of using the sub-chart:

    Set `postgresql.enabled` to `true`.
    The other `postgresql.*` values are rather arbitrary in this case and will be
    passed to the PostgreSQL instance and the other sub-charts.

  - In case of using another PostgreSQL instance:

    Set `postgresql.enabled` to `false`.
    Fill the server location in `postgresql.connection.(host|port)`
    and the credentials of the external instance in `postgresql.auth.(database|username|password)`.

- In any case, ensure that `proxy.ingress.host` is set to the desired SSO hostname.

- Note: Captcha protection is disabled by default.

  In order to enable it
  ensure that the chosen Keycloak image or host contains our extension plugin
  and set `handler.appConfig.captchaProtectionEnable` to `"true"`.

Install the chart as follows:

```bash
helm upgrade --install --namespace <YOUR_NAMESPACE> --values <YOUR_VALUES.YAML> keycloak-extensions .
```

Then follow [the instructions](https://git.knut.univention.de/univention/customers/dataport/upx/pocs/keycloak-extensions#setup)
to configure the realm properly and enable the reCaptha-protected auth fow.

# Helm docs

# keycloak-extensions

![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: 21.0.1](https://img.shields.io/badge/AppVersion-21.0.1-informational?style=flat-square)

A Helm chart for Kubernetes with its extensions

**Homepage:** <https://www.univention.de/>

## Requirements

| Repository | Name | Version |
|------------|------|---------|
| file://./charts/handler | handler | 0.1.0 |
| file://./charts/proxy | proxy | 0.1.0 |
| https://charts.bitnami.com/bitnami | common | ^2.2.2 |
| https://charts.bitnami.com/bitnami | postgresql | ^12.2.2 |

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| global | object | `{"keycloak":{"adminPassword":"univention","adminRealm":null,"adminUsername":"admin","host":"keycloak","realm":"ucs"},"postgresql":{"auth":{"database":"bfp","password":"correcthorsebatterystaple","postgresPassword":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}}` | Global Keycloak Extensions configuration values |
| global.keycloak | object | `{"adminPassword":"univention","adminRealm":null,"adminUsername":"admin","host":"keycloak","realm":"ucs"}` | External Keycloak settings |
| global.keycloak.adminPassword | string | `"univention"` | Admin password for Keycloak admin-cli provided user |
| global.keycloak.adminUsername | string | `"admin"` | Admin user for Keycloak admin-cli |
| global.keycloak.host | string | `"keycloak"` | Host where keycloak is accessible (specify port if needed) |
| global.keycloak.realm | string | `"ucs"` | Keycloak realm to listen events on (master allows to listen for all realms) |
| global.postgresql | object | `{"auth":{"database":"bfp","password":"correcthorsebatterystaple","postgresPassword":"correcthorsebatterystaple","username":"bfp"},"connection":{"host":"keycloak-extensions-postgresql","port":"5432"}}` | PostgreSQL settings |
| global.postgresql.auth | object | `{"database":"bfp","password":"correcthorsebatterystaple","postgresPassword":"correcthorsebatterystaple","username":"bfp"}` | Authentication details |
| global.postgresql.auth.database | string | `"bfp"` | Database for the proxy and handler to use |
| global.postgresql.auth.password | string | `"correcthorsebatterystaple"` | Password for the PostgreSQL database |
| global.postgresql.auth.postgresPassword | string | `"correcthorsebatterystaple"` | Currently unused |
| global.postgresql.auth.username | string | `"bfp"` | User for the PostgreSQL database |
| global.postgresql.connection | object | `{"host":"keycloak-extensions-postgresql","port":"5432"}` | Connextion details |
| global.postgresql.connection.host | string | `"keycloak-extensions-postgresql"` | Hostname or IP address of the server hosting the PostgreSQL database |
| global.postgresql.connection.port | string | `"5432"` | Port number that the PostgreSQL database is exposed on |
| handler.appConfig.captchaProtectionEnable | string | `"false"` |  |
| handler.appConfig.mailFrom | string | `"univention@example.org"` |  |
| handler.appConfig.smtpHost | string | `"mail.example.org"` |  |
| handler.appConfig.smtpPassword | string | `"some_password"` |  |
| handler.appConfig.smtpPort | string | `"587"` |  |
| handler.appConfig.smtpUsername | string | `"univention"` |  |
| handler.image.tag | string | `"latest"` |  |
| postgresql | object | `{"enabled":true}` | PostgreSQL settings.  The bitnami helm chart does contain all details of what can be configured: https://github.com/bitnami/charts/tree/main/bitnami/postgresql |
| postgresql.enabled | bool | `true` | Set to `true` if you want PostgreSQL to be installed as well. |
| proxy.appConfig.captchaSiteKey | string | `"some_site_key"` |  |
| proxy.image.tag | string | `"latest"` |  |
| proxy.ingress.host | string | `"sso.example.com"` |  |
