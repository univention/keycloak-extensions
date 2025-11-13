# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import \
    AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import \
    AuthSecretGenerationUser
from univention.testing.helm.auth_flavors.username import AuthUsernameViaEnv, pytest
from univention.testing.helm.client.base import BaseTest


class TestSmtpSecret(AuthSecretGenerationUser, AuthPasswordUsageViaEnv, AuthUsernameViaEnv):
    secret_name = "release-name-keycloak-extensions-smtp-credentials"
    prefix_mapping = {
        "smtp.auth": "auth"
    }
    sub_path_env_password = "env[?@name=='SMTP_PASSWORD']"
    workload_name = "release-name-keycloak-extensions-handler"
    sub_path_env_username = "env[?@name=='SMTP_USERNAME']"


class TestSmtpSecretNotTemplatedIfAuthDisabled(BaseTest):
    def test_env_vars_not_templated(self, chart):
        values = self.load_and_map(
            """
            smtp:
              auth:
                enabled: false
                password: null
                existingSecret:
                  name: null
            """)
        result = chart.helm_template(values)

        smtp_username = "env[?@name=='SMTP_USERNAME']"
        smtp_password = "env[?@name=='SELF_PASSWORD']"

        workload = result.get_resource(
            kind="Deployment", name="release-name-keycloak-extensions-handler")
        container = workload.findone(self.path_container)

        with pytest.raises(LookupError):
            container.findone(smtp_username)

        with pytest.raises(LookupError):
            container.findone(smtp_password)

    def test_secret_not_templated(self, chart):
        values = self.load_and_map(
            """
            smtp:
              auth:
                enabled: false
                password: null
                existingSecret:
                  name: null
            """)
        result = chart.helm_template(values)

        with pytest.raises(LookupError):
            result.get_resource(
                kind="Secret", name="release-name-keycloak-extensions-smtp-credentials")
