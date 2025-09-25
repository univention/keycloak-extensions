# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from univention.testing.helm.auth_flavors.password_usage import \
    AuthPasswordUsageViaEnv
from univention.testing.helm.auth_flavors.secret_generation import \
    AuthSecretGenerationUser
from univention.testing.helm.auth_flavors.username import AuthUsernameViaEnv


class SettingsTestKeycloakSecret:
    secret_name = "release-name-keycloak-extensions-keycloak-credentials"
    prefix_mapping = {"keycloak.auth": "auth"}

    # Used by AuthSecretGenerationUser only
    path_password = "stringData.adminPassword"

    # Used by AuthSecretGenerationUser and AuthUsernameViaEnv only
    sub_path_env_password = "env[?@name=='KC_PASS']"
    sub_path_env_username = "env[?@name=='KC_USER']"
    secret_default_key = "adminPassword"


class TestChartCreatesKeycloakSecretAsUser(SettingsTestKeycloakSecret, AuthSecretGenerationUser):
    pass


class TestHandlerUsesKeycloakCredentialsByEnv(SettingsTestKeycloakSecret, AuthPasswordUsageViaEnv, AuthUsernameViaEnv):
    workload_name = "release-name-keycloak-extensions-handler"


class TestProxyUsesKeycloakCredentialsByEnv(SettingsTestKeycloakSecret, AuthPasswordUsageViaEnv, AuthUsernameViaEnv):
    workload_name = "release-name-keycloak-extensions-proxy"
