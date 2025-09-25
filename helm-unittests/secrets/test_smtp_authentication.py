# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import \
    AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import \
    AuthSecretGenerationUser
from univention.testing.helm.auth_flavors.username import AuthUsernameViaEnv


class TestSmtpSecret(AuthSecretGenerationUser, AuthPasswordUsageViaEnv, AuthUsernameViaEnv):
    secret_name = "release-name-keycloak-extensions-smtp-credentials"
    prefix_mapping = {
        "smtp.auth": "auth"
    }
    sub_path_env_password = "env[?@name=='SMTP_PASSWORD']"
    workload_name = "release-name-keycloak-extensions-handler"
    sub_path_env_username = "env[?@name=='SMTP_USERNAME']"
