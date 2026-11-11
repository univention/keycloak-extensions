# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from models.device import Device
from modules.notifier import Notifier, session_id_from_device_id


@pytest.fixture
def keycloak_mock():
    mock = MagicMock()
    mock.get_user.return_value = {
        "username": "jdoe",
        "firstName": "Jane",
        "lastName": "Doe",
        "email": "test@example.com",
    }
    return mock


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def device():
    device = Device(
        keycloak_device_id="device123",
        fingerprint_device_id="fingerprint123",
        user_id="user123",
        is_notified=False,
    )
    device.created_at = datetime(2024, 5, 20, 12, 0, 0, tzinfo=timezone.utc)
    return device


@pytest.mark.parametrize("timezone,valid,expected_hour", [
    ("UTC", True, 12),  # Default timezone
    ("Europe/Berlin", True, 14),  # UTC+2 in summer
    ("Asia/Tokyo", True, 21),  # UTC+9
    ("Etc/GMT+2", True, 10),  # UTC-2
    ("Africa/Nairobi", True, 15),  # UTC+3
    ("InvalidZone", False, 12),  # Invalid timezone should fallback to UTC
])
@patch("modules.notifier.mail.Email")
@patch("modules.notifier.session", new_callable=MagicMock)
def test_notify_new_logins_timezones(mock_session, mock_email_class, device, timezone, valid, expected_hour, keycloak_mock):
    # Set ENV variable for timezone
    os.environ["EMAIL_TIMEZONE"] = timezone

    mock_email_instance = MagicMock()
    mock_email_class.return_value = mock_email_instance

    # Mock database query
    mock_session.query.return_value.filter.return_value.all.return_value = [
        device]

    # Create Notifier instance
    notifier = Notifier(keycloak_mock)
    notifier.notify_new_logins()

    # Verify that Email was created with the correct details
    mock_email_class.assert_called_once()
    args, _ = mock_email_class.call_args

    # First argument should be the email address
    assert args[0] == "test@example.com"

    # Second argument should be the details dict
    details = args[1]
    expected_timezone = timezone if valid else "UTC"
    # Check for correct hour based on timezone
    expected_time = f"2024-05-20 {expected_hour}:00:00 ({expected_timezone})"
    assert details == {
        "time": expected_time,
        "device_id": "device123",
        "full_name": "Jane Doe",
    }

    # Verify that send was called
    mock_email_instance.send.assert_called_once()


@pytest.mark.parametrize("first_name,last_name,expected", [
    ("Jane", "Doe", "Jane Doe"),
    ("", "Doe", "Doe"),
    (None, "Doe", "Doe"),
    ("  Jane ", " Doe", "Jane Doe"),
])
@patch("modules.notifier.mail.Email")
def test_notify_user_full_name(mock_email_class, keycloak_mock, first_name, last_name, expected):
    user = {"username": "jdoe", "lastName": last_name,
            "email": "test@example.com"}
    if first_name is not None:
        user["firstName"] = first_name
    keycloak_mock.get_user.return_value = user

    Notifier(keycloak_mock).notify_user(
        "user123", {"time": "2024-05-20 12:00:00 (UTC)", "device_id": "device123"})

    args, _ = mock_email_class.call_args
    assert args[1]["full_name"] == expected
    assert "username" not in args[1]


@patch("modules.notifier.mail.Email")
def test_notify_user_without_email(mock_email_class, keycloak_mock):
    keycloak_mock.get_user.return_value = {
        "username": "jdoe", "lastName": "Doe"}

    Notifier(keycloak_mock).notify_user(
        "user123", {"time": "2024-05-20 12:00:00 (UTC)", "device_id": "device123"})

    mock_email_class.assert_not_called()


@pytest.mark.parametrize("device_id,expected", [
    # Keycloak 26: Base64 of "<session ID>.<signature>"
    ("TmcwdnZsZVV5Q1ZsZ1pGWmJaUUJhWk5nLmFGbjVtWTZfbXVoWnVvNVpVQllvNlRWV3JFVDM5Nm1Vc0FMdHRTd0VaNk9kVlZHcTZBV213amR3VENqVkhBaDJMajctS19UZFJtY2VUaDVQc3FfV25R",
     "Ng0vvleUyCVlgZFZbZQBaZNg"),
    # Older Keycloak: plain session ID
    ("Ng0vvleUyCVlgZFZbZQBaZNg", "Ng0vvleUyCVlgZFZbZQBaZNg"),
    ("4f6b1c2e-0d1a-4b8e-9a51-6f0e1d2c3b4a",
     "4f6b1c2e-0d1a-4b8e-9a51-6f0e1d2c3b4a"),
    ("device123", "device123"),
    ("", ""),
])
def test_session_id_from_device_id(device_id, expected):
    assert session_id_from_device_id(device_id) == expected
