# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

"""Tests that the proxy forwards requests to Keycloak unchanged.

Regression tests for the http-proxy-middleware v2 -> v3 migration, where
`pathFilter: "**"` stopped matching paths with dot-segments (micromatch
matches globs with dot:false by default), so requests such as
/realms/<realm>/.well-known/openid-configuration were answered by the
proxy with a 404 instead of reaching Keycloak.
"""

import base64
import hashlib
import secrets

import requests

REQUEST_TIMEOUT = 30


def test_openid_configuration_discovery(base_url, realm):
    """Dotted path segments (.well-known) must reach Keycloak."""
    r = requests.get(
        f"{base_url}/realms/{realm}/.well-known/openid-configuration",
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    discovery = r.json()
    # Make sure the answer is the actual Keycloak discovery document.
    assert f"/realms/{realm}" in discovery["issuer"]
    assert discovery["authorization_endpoint"].endswith(
        f"/realms/{realm}/protocol/openid-connect/auth"
    )
    assert discovery["token_endpoint"].endswith(
        f"/realms/{realm}/protocol/openid-connect/token"
    )


def test_realm_endpoint_reaches_keycloak(base_url, realm):
    """Regular Keycloak paths must be proxied to Keycloak."""
    r = requests.get(
        f"{base_url}/realms/{realm}",
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    body = r.json()
    assert body["realm"] == realm
    assert body["public_key"]


def test_jwks_endpoint_reaches_keycloak(base_url, realm):
    """The JWKS certs endpoint must be proxied to Keycloak."""
    r = requests.get(
        f"{base_url}/realms/{realm}/protocol/openid-connect/certs",
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    assert len(r.json()["keys"]) > 0


def test_login_page_reaches_keycloak(base_url, realm):
    """The OIDC login form must be proxied and get FingerprintJS injected."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(
            code_verifier.encode()).digest())
        .rstrip(b"=")
        .decode()
    )
    r = requests.get(
        f"{base_url}/realms/{realm}/protocol/openid-connect/auth",
        params={
            "client_id": "security-admin-console",
            "response_type": "code",
            "scope": "openid",
            "redirect_uri": f"{base_url}/admin/{realm}/console/",
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        },
        timeout=REQUEST_TIMEOUT,
    )
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]
    # The proxy intercepts the login form and injects the FingerprintJS
    # script (see proxy/utils/injectors.js).
    assert "fingerprintjs" in r.text
