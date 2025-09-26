# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import \
    AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import \
    AuthSecretGenerationUser


class TestChartCreatesCaptchaSiteKeyAsUser(AuthSecretGenerationUser):
    secret_name = "release-name-keycloak-extensions-captcha-credentials"
    # The captcha site key is actually a user name stored in a secret.
    # Using the password generation test as base class is the easiest way
    # to test this.
    prefix_mapping = {
        "auth.captchaSiteKey": "auth.password",
        "proxy.appConfig.captcha": "auth",
    }
    path_password = "stringData.site_key"


class TestChartCreatesCaptchaSecretKeyAsUser(AuthSecretGenerationUser):
    secret_name = "release-name-keycloak-extensions-captcha-credentials"
    prefix_mapping = {
        "auth.captchaSecretKey": "auth.password",
        "proxy.appConfig.captcha": "auth",
    }
    path_password = "stringData.secret_key"


class SettingsProxyUsesCaptchaSecrets:
    prefix_mapping = {
        "proxy.appConfig.captcha": "auth",
    }
    secret_name = "release-name-keycloak-extensions-captcha-credentials"
    workload_name = "release-name-keycloak-extensions-proxy"


class TestProxyUsesCaptchaSecretKeyViaEnv(SettingsProxyUsesCaptchaSecrets, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='CAPTCHA_SECRET_KEY']"
    secret_default_key = "secret_key"


class TestProxyUsesCaptchaSiteKeyViaEnv(SettingsProxyUsesCaptchaSecrets, AuthPasswordUsageViaEnv):
    sub_path_env_password = "env[?@name=='CAPTCHA_SITE_KEY']"
    secret_default_key = "site_key"
    secret_default_key = "site_key"
