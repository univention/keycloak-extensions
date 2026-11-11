# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

from univention.testing.helm.client.base import BaseTest

CONFIGMAP_NAME = "release-name-keycloak-extensions-handler"


class TestNewDeviceLoginNotification(BaseTest):

    def render(self, chart, values_yaml=""):
        values = self.load_and_map(values_yaml)
        result = chart.helm_template(values)
        return result.get_resource(kind="ConfigMap", name=CONFIGMAP_NAME)

    def test_default_subject_contains_fqdn_placeholder(self, chart):
        configmap = self.render(chart)
        assert configmap.findone("data.NEW_DEVICE_LOGIN_SUBJECT") == \
            "Recent sign-in to a Nubus account on {fqdn}"

    def test_subject_with_quotes_is_rendered_verbatim(self, chart):
        configmap = self.render(chart, """
            handler:
              appConfig:
                newDeviceLoginSubject: 'New "sign-in" on {fqdn}'
            """)
        assert configmap.findone(
            "data.NEW_DEVICE_LOGIN_SUBJECT") == 'New "sign-in" on {fqdn}'

    def test_instance_fqdn_is_empty_without_host(self, chart):
        configmap = self.render(chart)
        assert configmap.findone("data.INSTANCE_FQDN") == ""

    def test_instance_fqdn_defaults_to_proxy_ingress_host(self, chart):
        configmap = self.render(chart, """
            proxy:
              ingress:
                host: "sso.example.org"
            """)
        assert configmap.findone("data.INSTANCE_FQDN") == "sso.example.org"

    def test_instance_fqdn_defaults_to_global_domain_in_nubus(self, chart):
        configmap = self.render(chart, """
            global:
              nubusDeployment: true
              domain: "example.org"
              subDomains:
                keycloak: "id"
            """)
        assert configmap.findone("data.INSTANCE_FQDN") == "id.example.org"

    def test_instance_fqdn_explicit_value_wins(self, chart):
        configmap = self.render(chart, """
            global:
              nubusDeployment: true
              domain: "example.org"
              subDomains:
                keycloak: "id"
            handler:
              appConfig:
                instanceFqdn: "portal.example.org"
            """)
        assert configmap.findone("data.INSTANCE_FQDN") == "portal.example.org"
