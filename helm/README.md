# Helm Chart for Keycloak with Brute Force Prevention PoC

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

  - Decide whether to use the Keycloak and its extensions from the sub-chart, or provide your own.

    - In case of using the sub-chart:

      Set `service.enabled` to `true` and configure `global.keycloak.*` to your liking.
      You will need the credentials for the manual configuration steps below.

    - In case of using another Keycloak instance:

      Set `service.enabled` to `false` and configure `global.keycloak.*`
      according to the external Keycloak's settings.

  - In any case, ensure that `proxy.ingress.host` is set to the desired SSO hostname.

  - Note: Captcha protection is disabled by default.

    In order to enable it
    ensure that the chosen Keycloak image or host contains our extension plugin
    and set `handler.appConfig.captchaProtectionEnable` to `"true"`.

Install the chart as follows:

```bash
helm install --replace --namespace <YOUR_NAMESPACE> --values <YOUR_VALUES.YAML> keycloak-extensions .
```

Then follow [the instructions](https://git.knut.univention.de/univention/customers/dataport/upx/pocs/keycloak-extensions#setup)
to configure the realm properly and enable the reCaptha-protected auth fow.
