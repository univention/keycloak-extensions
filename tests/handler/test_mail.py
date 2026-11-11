# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import pytest
from modules import mail

DETAILS = {
    "full_name": "Jane Doe",
    "time": "2024-05-20 12:00:00 (UTC)",
    "device_id": "4f6b1c2e-0d1a-4b8e-9a51-6f0e1d2c3b4a",
}


def body_of(email):
    return email.message.get_payload()[0].get_payload(decode=True).decode("utf-8")


def test_subject_contains_fqdn():
    email = mail.Email("jane.doe@example.org", DETAILS)
    assert email.message["Subject"] == "Recent sign-in to a Nubus account on id.example.org"


def test_body_contains_details():
    body = body_of(mail.Email("jane.doe@example.org", DETAILS))
    assert "Information about recent account activity" in body
    assert "  Account:   Jane Doe\n" in body
    assert "  E-mail:    jane.doe@example.org\n" in body
    assert "  Instance:  id.example.org\n" in body
    assert "  Time:      2024-05-20 12:00:00 (UTC)\n" in body
    assert "This message was sent automatically by Nubus at id.example.org." in body
    assert body.rstrip().endswith("Device ID: 4f6b1c2e-0d1a-4b8e-9a51-6f0e1d2c3b4a")


def test_body_does_not_leak_internals():
    body = body_of(mail.Email("jane.doe@example.org", DETAILS))
    assert "Keycloak" not in body
    assert "Fingerprint" not in body


def test_body_is_utf8():
    email = mail.Email("joerg@example.org",
                       {**DETAILS, "full_name": "Jörg Müller"})
    assert email.message.get_payload()[0].get_content_charset() == "utf-8"
    assert "  Account:   Jörg Müller\n" in body_of(email)


def test_default_subject(monkeypatch):
    monkeypatch.delenv("NEW_DEVICE_LOGIN_SUBJECT", raising=False)
    email = mail.Email("jane.doe@example.org", DETAILS)
    assert email.message["Subject"] == "Recent sign-in to a Nubus account on id.example.org"


@pytest.mark.parametrize("subject,expected", [
    ("New device login", "New device login"),
    ("[{fqdn}] New sign-in", "[id.example.org] New sign-in"),
    ("Sign-in {unknown}", "Sign-in {unknown}"),
    ("Sign-in {", "Sign-in {"),
    ("Sign-in {0}", "Sign-in {0}"),
])
def test_custom_subject(monkeypatch, subject, expected):
    monkeypatch.setenv("NEW_DEVICE_LOGIN_SUBJECT", subject)
    email = mail.Email("jane.doe@example.org", DETAILS)
    assert email.message["Subject"] == expected


def test_fqdn_falls_back_to_keycloak_url(monkeypatch):
    monkeypatch.setenv("INSTANCE_FQDN", "")
    monkeypatch.setenv("KC_AUTH_URL", "http://nubus-keycloak:8080/admin")
    assert mail.get_instance_fqdn() == "nubus-keycloak"
